"""Check one existing section plan; no rendering, uploads or plan mutations.

Usage: plan_check.py PLAN [--source SOURCE] [--route mac|cloud] [--final]
SOURCE is the unchanged MEGAPHONE SECTIONS export or JSON {sections:[id,start,end]}.
Omitting SOURCE is for historical diagnostics only; identity is UNAVAILABLE (exit 2).
"""
import argparse
import json
import math
from pathlib import Path
import re
import statistics
import struct
import subprocess
import sys

POLICY = Path(__file__).resolve().parents[1] / 'plugins/megaphone/skills/motion-graphics/references/edit-rules.json'


def source_sections(path):
    text = path.read_text()
    if text.lstrip().startswith('{'):
        return json.loads(text)['sections']
    rows = []
    for line in text.splitlines():
        fields = [field.strip() for field in line.split('|')]
        if len(fields) < 4 or not fields[0].isdigit():
            continue
        timing = re.fullmatch(r'([\d.]+)\s*[-–]\s*([\d.]+)\s*s', fields[1])
        if timing is None or not fields[2].startswith('id='):
            raise ValueError('Malformed source section')
        content = fields[4:] if fields[3].startswith('line=') else fields[3:]
        rows.append(dict(id=fields[2][3:], start=float(timing[1]), end=float(timing[2]), text=' | '.join(content)))
    if not rows:
        raise ValueError('No source sections found')
    return rows


def finite(value):
    return type(value) in (float, int) and math.isfinite(value)


def media_tag(path):
    if path.suffix.lower() == '.png':
        data = path.read_bytes()
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('Invalid PNG')
        pos = 8
        while pos + 12 <= len(data):
            size = struct.unpack('>I', data[pos:pos + 4])[0]
            chunk = data[pos + 8:pos + 8 + size]
            if data[pos + 4:pos + 8] == b'tEXt' and chunk.startswith(b'Comment\0'):
                return json.loads(chunk.split(b'\0', 1)[1]), None
            pos += size + 12
        raise ValueError('Missing PNG Comment tag')
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                             'format=duration:format_tags=comment', '-of', 'json', str(path)],
                            capture_output=True, text=True, check=True, timeout=30)
    info = json.loads(result.stdout)['format']
    return json.loads(info['tags']['comment']), float(info['duration'])


def check(plan, policy, source=None, route='mac', media_root=None):
    failures, warnings, unavailable = [], [], []
    if not isinstance(plan, dict):
        return ['Plan must be an object'], [], []
    sections = plan.get('sections')
    if type(plan.get('v')) is not int or plan['v'] not in (2, 3, 4) or not isinstance(sections, list) or not sections:
        return ['Unsupported/empty section plan (supported: v2, v3, v4)'], [], []
    if not isinstance(plan.get('set'), str) or re.fullmatch('[a-z0-9-]{1,60}', plan['set']) is None:
        return ['Invalid/missing media set'], [], []
    if plan.get('hookCard') is not None and not isinstance(plan['hookCard'], dict):
        return ['Invalid hook card'], [], []
    allowed = {'face', 'split', 'full'} | ({'overlay', 'greenscreen', 'shrink'} if route == 'mac' else set())
    ids, cursor = set(), 0.0
    for s in sections:
        if not isinstance(s, dict) or not isinstance(s.get('id'), str) or not s['id'].strip():
            failures.append('Section must have a nonempty ID'); continue
        if s['id'] in ids:
            failures.append('Duplicate section ID: ' + s['id'])
        ids.add(s['id'])
        a, b = s.get('start'), s.get('end')
        if not finite(a) or not finite(b) or a < 0 or b <= a:
            failures.append('Invalid section times: ' + s['id']); continue
        if abs(a - cursor) > 0.02:
            failures.append('Gap, overlap or unordered section: ' + s['id'])
        cursor = b
        layout = s.get('layout')
        if layout not in allowed:
            failures.append('Unsupported layout: ' + s['id'])
        name = s.get('image') if layout == 'greenscreen' else s.get('clip')
        # Breakdown (style=breakdown): the phone draws a `card` itself, and `shrink` needs no file.
        drawn = layout == 'shrink' or (layout in ('split', 'full') and isinstance(s.get('card'), dict) and not name)
        if layout != 'face' and not drawn and (not isinstance(name, str) or not name):
            failures.append('Missing media identity: ' + s['id'])
        if layout == 'face' and (s.get('clip') or s.get('image')):
            failures.append('Face section still references media: ' + s['id'])
        if name and (Path(name).name != name or name in ('.', '..')):
            failures.append('Media must be a local filename: ' + s['id'])
        if s.get('zoom') is not None and s['zoom'] not in ('punchIn', 'gradual', 'punch', 'jump'):
            failures.append('Unsupported zoom: ' + s['id'])
        if s.get('transition') is not None and s['transition'] not in ('cut', 'fade', 'pop'):
            failures.append('Unsupported transition: ' + s['id'])
        if s.get('look') is not None and (s['look'] not in ('bold', 'coolGirl', 'coolDude') or s['look'] == plan.get('style')):
            failures.append('Unsupported look (or same as the plan style): ' + s['id'])
        word = s.get('word')
        if word is not None:
            key = lambda t: re.sub(r'[^\w]', '', str(t)).lower()
            if (layout != 'overlay' and not s.get('top') and not s.get('sticker')
                    and not isinstance(s.get('card'), dict)) \
                    or not isinstance(word, str) or not key(word) \
                    or key(word) not in [key(t) for t in str(s.get('text', '')).split()]:
                failures.append('Word must be one word of an overlay section: ' + s['id'])
        frame = s.get('frame') if isinstance(s.get('frame'), dict) else {}
        if frame.get('anchor') not in (None, 'head') or (frame.get('anchor') == 'head' and s.get('behind') is not True):
            failures.append('Head anchor needs behind: true (and anchor must be "head"): ' + s['id'])
        top = s.get('top')
        if top is not None:
            key = lambda t: re.sub(r'[^\w]', '', str(t)).lower()
            words = [key(t) for t in str(s.get('caption') or s.get('text', '')).split()]
            if not isinstance(top, str) or not top.strip() or any(key(t) not in words for t in top.split()):
                failures.append('Top word must be words of the section: ' + s['id'])
        sticker = s.get('sticker')
        if sticker is not None:
            key = lambda t: re.sub(r'[^\w]', '', str(t)).lower()
            words = [key(t) for t in str(s.get('caption') or s.get('text', '')).split()]
            if not isinstance(sticker, str) or len(sticker.split()) != 1 or key(sticker) not in words:
                failures.append('Sticker must be one word of the section: ' + s['id'])
        if s.get('mark') is not None and (s['mark'] not in ('circle', 'strike')
                                          or (s['mark'] == 'circle' and layout != 'shrink')
                                          or (s['mark'] == 'strike' and not top)):
            failures.append('Mark: circle needs shrink, strike needs top: ' + s['id'])
    # Behind-head words need the phone's cutout, which a green screen turns off for the whole video.
    # (A split clip only turns it off while the split is on screen, and a behind word is never a split.)
    if any(isinstance(s, dict) and s.get('behind') is True for s in sections) and any(
            isinstance(s, dict) and s.get('layout') == 'greenscreen' for s in sections):
        failures.append('Behind-head words need a plan with no green screen')
    if failures:
        return failures, warnings, unavailable
    if source is None:
        unavailable.append('Source identity/timing (historical diagnostic only)')
    elif (not isinstance(source, list) or not all(isinstance(q, dict) for q in source) or len(source) != len(sections) or any(
            p['id'] != q.get('id') or not finite(q.get('start')) or not finite(q.get('end'))
            or abs(p['start'] - q['start']) > 0.001 or abs(p['end'] - q['end']) > 0.001
            or ('text' in q and p.get('text') != q['text'])
            for p, q in zip(sections, source))):
        failures.append('Plan differs from supplied section IDs/timing/text/order')
    total = sections[-1]['end']
    full_run = full = face = 0.0
    shots = []
    previous = None
    for s in sections:
        duration = s['end'] - s['start']
        key = (s['layout'], s.get('clip') or s.get('image') or json.dumps(s.get('card'), sort_keys=True))
        if key == previous:
            shots[-1] += duration
        else:
            shots.append(duration)
        previous = key
        full_run = full_run + duration if s['layout'] == 'full' else 0
        if full_run > policy['maximumFaceAbsence'] + 0.001:
            failures.append('Continuous full graphics over limit at ' + s['id'])
        full += duration if s['layout'] == 'full' else 0
        face += duration if s['layout'] in ('face', 'shrink') else 0
        if media_root is not None and s['layout'] not in ('face', 'shrink') and (s.get('clip') or s.get('image')):
            name = s.get('image') if s['layout'] == 'greenscreen' else s['clip']
            path = media_root / name
            try:
                if not path.is_file() or path.resolve().parent != media_root.resolve():
                    raise ValueError('Missing/outside media file')
                tag, available = media_tag(path)
                if (type(tag.get('n')) is not int or type(tag.get('of')) is not int
                        or not 1 <= tag['n'] <= tag['of'] or tag.get('v') != 1
                        or not isinstance(tag.get('text'), str) or not tag['text'].strip()):
                    raise ValueError('Invalid phone media tag')
                prefix = {'greenscreen': 'gs', 'overlay': 'mo'}.get(s['layout'], 'mb')
                suffix = 'png' if s['layout'] == 'greenscreen' else 'mp4'
                expected_name = f'{prefix}-{tag.get("set")}-{tag["n"]:02d}of{tag["of"]:02d}.{suffix}'
                if name != expected_name or ('text' in s and tag['text'] != s['text']):
                    raise ValueError('Filename/text differs from phone tag')
                expected_place = {'overlay': 'overlay', 'full': 'full'}.get(s['layout'], 'split')
                if (tag.get('section') != s['id'] or tag.get('set') != plan.get('set')
                        or (s['layout'] != 'greenscreen' and tag.get('place', 'split') != expected_place)):
                    raise ValueError('Media section/set/layout tag mismatch')
                if available is not None and (not finite(available) or available + 1 / 30 < duration):
                    raise ValueError('Clip shorter than its section')
                if s.get('gate') != 'pass':
                    raise ValueError('Final section has no passing clip gate')
            except (ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
                failures.append(f'Media check {s["id"]}: {type(e).__name__}: {e}')
    if min(shots) < policy['minimumShot'] or max(shots) > policy['maximumShot']:
        warnings.append('Shot length outside preference')
    if statistics.median(shots) > policy['maximumMedianShot']:
        warnings.append('Median shot above preference')
    if full / total > policy['maximumFullShare']:
        warnings.append('Full graphic share above preference')
    if not policy['minimumFaceOnlyShare'] <= face / total <= policy['maximumFaceOnlyShare']:
        warnings.append('Face-only share outside preference')
    rate = (len(shots) - 1) / total * policy['switchWindow']
    if not policy['minimumSwitches'] <= rate <= policy['maximumSwitches']:
        warnings.append('Visual switch rate outside preference')
    if sections[0]['layout'] == 'face' and not (plan.get('hookCard') or {}).get('lines'):
        warnings.append('Opening graphic/hook not planned')
    unavailable.extend(['Actual face visibility, animation events and proof truth (visual review)',
                        f'Planned camera-visible share: {1 - full / total:.1%} (not face detection)'])
    return failures, warnings, unavailable


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--route', choices=['mac', 'cloud'], default='mac')
    parser.add_argument('--final', action='store_true')
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text())
        if not isinstance(plan, dict):
            raise ValueError('Plan must be an object')
        failures, warnings, unavailable = check(plan, json.loads(POLICY.read_text()),
            source_sections(args.source) if args.source else None, args.route,
            args.plan.parent if args.final else None)
        if args.final and not args.source:
            failures.append('Final delivery requires --source')
        for label, values in [('FAIL', failures), ('WARN', warnings), ('UNAVAILABLE', unavailable)]:
            for value in values:
                print(f'{label} {value}')
        print('FAIL required checks' if failures else 'PASS required checks' if args.source else 'DIAGNOSTIC ONLY; source not verified')
        return 1 if failures else 0 if args.source else 2
    except (ValueError, KeyError, TypeError, OSError) as e:
        print(f'FAIL invalid input: {e}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
