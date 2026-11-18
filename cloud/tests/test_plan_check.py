import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('plan_check', ROOT / 'plan_check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
POLICY = json.loads(checker.POLICY.read_text())


def plan(layouts=('split', 'face', 'full')):
    return {'v': 4, 'set': 'motion-abc123', 'sections': [
        dict(id=str(i), start=i * 2, end=(i + 1) * 2, layout=layout,
             clip=None if layout == 'face' else f'mb-motion-abc123-{i + 1:02d}of03.mp4')
        for i, layout in enumerate(layouts)]}


class PlanCheckTests(unittest.TestCase):
    def test_complete_source(self):
        p = plan()
        self.assertEqual(checker.check(p, POLICY, p['sections'])[0], [])

    def test_source_identity_and_times_are_required(self):
        for field, value in [('id', 'different'), ('end', 2.1)]:
            p = plan(); source = copy.deepcopy(p['sections']); source[0][field] = value
            self.assertTrue(checker.check(p, POLICY, source)[0])

    def test_unsupported_and_empty_are_not_pass(self):
        for p in [{'beats': []}, {'v': 4, 'sections': []}, {'v': 5, 'sections': [{}]}]:
            self.assertTrue(checker.check(p, POLICY)[0])

    def test_nonfinite_overlap_duplicate_and_unknown_layout(self):
        for key, value in [('start', float('nan')), ('end', float('inf')), ('start', 0.1), ('id', '1'), ('layout', 'invented')]:
            p = plan(); p['sections'][0][key] = value
            self.assertTrue(checker.check(p, POLICY)[0])

    def test_punch_jump_transition_and_behind_word(self):
        p = plan(('face', 'overlay', 'face'))
        p['sections'][0]['zoom'] = 'jump'
        p['sections'][2]['zoom'] = 'punch'
        o = p['sections'][1]
        o.update(clip='mo-motion-abc123-01of01.mp4', text='we chat for hours', word='chat', transition='pop',
                 frame={'x': 0.5, 'y': 0.27, 'w': 0.9, 'anchor': 'head'}, behind=True)
        self.assertEqual(checker.check(p, POLICY, route='mac')[0], [])
        for key, value in [('word', 'hours!'), ('word', 'missing'), ('transition', 'wipe'), ('behind', False)]:
            q = copy.deepcopy(p); q['sections'][1][key] = value
            self.assertEqual(bool(checker.check(q, POLICY, route='mac')[0]), key != 'word' or value != 'hours!', (key, value))
        q = copy.deepcopy(p); q['sections'][0]['zoom'] = 'dolly'
        self.assertTrue(checker.check(q, POLICY, route='mac')[0])
        # Behind words next to a split clip are fine: the cutout is off only during the split.
        q = copy.deepcopy(p); q['sections'][2].update(layout='split', clip='mb-motion-abc123-01of01.mp4', zoom=None)
        self.assertNotIn('Behind-head words need a plan with no green screen', checker.check(q, POLICY, route='mac')[0])
        # Behind words and a green screen in one plan: the phone's cutout would be off.
        q = copy.deepcopy(p); q['sections'][2].update(layout='greenscreen', image='gs-abc123-01of01.png', clip=None, zoom=None)
        self.assertIn('Behind-head words need a plan with no green screen', checker.check(q, POLICY, route='mac')[0])

    def test_section_look(self):
        def look_failures(value, style=None):
            p = plan(); p['sections'][1]['look'] = value
            if style: p['style'] = style
            return [f for f in checker.check(p, POLICY)[0] if 'look' in f]
        self.assertEqual(look_failures('coolGirl'), [])
        self.assertEqual(look_failures(None), [])
        self.assertTrue(look_failures('neon'))
        self.assertTrue(look_failures('bold', style='bold'))

    def test_adjacent_full_clips_are_one_absence(self):
        self.assertTrue(checker.check(plan(('full', 'full', 'full')), POLICY)[0])

    def test_dropped_clip_is_face(self):
        p = plan(); p['sections'][2].update(layout='face', clip=None)
        self.assertEqual(checker.check(p, POLICY)[0], [])

    def test_same_layout_different_graphics_are_different_shots(self):
        p = plan(('split', 'split', 'split'))
        self.assertNotIn('Median shot above preference', checker.check(p, POLICY)[1])
        for s in p['sections']: s['clip'] = 'same.mp4'
        self.assertIn('Median shot above preference', checker.check(p, POLICY)[1])

    def test_missing_media_and_unsafe_paths_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertTrue(checker.check(plan(), POLICY, media_root=Path(folder))[0])
        p = plan(); p['sections'][0]['clip'] = '../escape.mp4'
        self.assertTrue(checker.check(p, POLICY)[0])

    def test_cloud_rejects_mac_only_layouts(self):
        self.assertTrue(checker.check(plan(('overlay',)), POLICY, route='cloud')[0])

    def test_source_export_parser(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'source.txt'
            source.write_text('MEGAPHONE SECTIONS v1\n01 | 0.00-2.00 s | id=one | line=0 | words')
            self.assertEqual(checker.source_sections(source), [dict(id='one', start=0.0, end=2.0, text='words')])

    def test_phone_policy_is_identical(self):
        phone = ROOT.parent.parent / 'MegaphoneApp/MegaphoneApp/Resources/EditRules.json'
        if not phone.exists():
            self.skipTest('Phone checkout absent; run policy parity in the app workspace')
        self.assertEqual(checker.POLICY.read_bytes(), phone.read_bytes())


    def test_final_tag_layout_duration_and_gate(self):
        with tempfile.TemporaryDirectory() as folder:
            p = plan(('split',))
            section = p['sections'][0]
            section.update(clip='mb-motion-abc123-01of01.mp4', gate='pass', text='words')
            (Path(folder) / section['clip']).touch()
            tag = dict(v=1, set=p['set'], section='0', place='split', text='words', n=1, of=1)
            for place, duration, gate, should_fail in [('split', 2, 'pass', False), ('full', 2, 'pass', True), ('split', 1, 'pass', True), ('split', 2, 'pending', True)]:
                section['gate'] = gate
                with patch.object(checker, 'media_tag', return_value=({**tag, 'place': place}, duration)):
                    self.assertEqual(bool(checker.check(p, POLICY, p['sections'], media_root=Path(folder))[0]), should_fail)

    def test_changed_source_words_fail(self):
        p = plan(); source = copy.deepcopy(p['sections']); source[0]['text'] = 'Changed words'
        self.assertTrue(checker.check(p, POLICY, source)[0])


    def test_diagnostic_only_exit_cannot_authorize_render(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'plan.json'; path.write_text(json.dumps(plan()))
            diagnostic = subprocess.run([sys.executable, str(ROOT / 'plan_check.py'), str(path)], capture_output=True, text=True)
            self.assertEqual(diagnostic.returncode, 2)
            self.assertNotIn('PASS required checks', diagnostic.stdout)
            source = Path(folder) / 'source.json'; source.write_text(json.dumps(plan()))
            verified = subprocess.run([sys.executable, str(ROOT / 'plan_check.py'), str(path), '--source', str(source)], capture_output=True, text=True)
            self.assertEqual(verified.returncode, 0)
            self.assertIn('PASS required checks', verified.stdout)

if __name__ == '__main__':
    unittest.main()


class BreakdownPlanTests(unittest.TestCase):
    """style=breakdown: the phone draws cards, the shrink and marks, so those sections have no file."""

    def sections(self):
        return [
            dict(id='a', start=0, end=2, layout='split', text='either it got hacked',
                 card={'kind': 'option', 'label': 'Option 1', 'title': 'hacked?'}),
            dict(id='b', start=2, end=4, layout='shrink', text='I do not believe in conspiracies',
                 top='conspiracies', mark='strike'),
            dict(id='c', start=4, end=6, layout='full', text='nine times out of ten it takes longer',
                 card={'kind': 'bars', 'bars': [{'label': 'a', 'value': 1}, {'label': 'b', 'value': 4}]}),
            dict(id='d', start=6, end=8, layout='face', text='that is my advice', top='my advice', word='advice'),
        ]

    def test_breakdown_plan_passes(self):
        p = {'v': 4, 'set': 'motion-abc123', 'style': 'breakdown', 'sections': self.sections()}
        failures, _, _ = checker.check(p, POLICY)
        self.assertEqual(failures, [])

    def test_top_word_must_be_said(self):
        sections = self.sections()
        sections[3]['top'] = 'secret sauce'
        failures, _, _ = checker.check({'v': 4, 'set': 'motion-abc123', 'sections': sections}, POLICY)
        self.assertIn('Top word must be words of the section: d', failures)

    def test_circle_needs_shrink(self):
        sections = self.sections()
        sections[0]['mark'] = 'circle'
        failures, _, _ = checker.check({'v': 4, 'set': 'motion-abc123', 'sections': sections}, POLICY)
        self.assertIn('Mark: circle needs shrink, strike needs top: a', failures)


class BreakdownStickerTests(unittest.TestCase):
    def test_sticker_must_be_a_word_of_the_line(self):
        sections = [dict(id='a', start=0, end=2, layout='face', text='they never tell you why', sticker='why?', word='why'),
                    dict(id='b', start=2, end=4, layout='face', text='so you guess', sticker='secret')]
        failures, _, _ = checker.check({'v': 4, 'set': 'motion-abc123', 'sections': sections}, POLICY)
        self.assertEqual(failures, ['Sticker must be one word of the section: b'])
