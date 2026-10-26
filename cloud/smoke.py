"""Bounded render proof, using a pinned upstream reference and no customer data.

Run: python3 cloud/smoke.py [new-output-directory]
Produces a 9 s, 1920x1080 MP4, three preview frames, a contact sheet and a JSON
receipt with actual metadata, decoding, motion checks and elapsed render time.
Never uploads, starts another run, or modifies the source composition.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'plugins/megaphone/skills/motion-graphics/upstream'
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'output/cloud-motion-smoke').resolve()
HF = ROOT / 'cloud/node_modules/.bin/hyperframes'


def run(*args, timeout=600):
    subprocess.run([str(a) for a in args], check=True, timeout=timeout)


def main():
    if OUT.exists():
        raise SystemExit(f'Choose a new output directory; preserving existing output: {OUT}')
    if not HF.exists():
        raise SystemExit('Install the runtime first: bash cloud/setup.sh')
    project = OUT / 'project'
    project.mkdir(parents=True)
    for name in ('index.html', 'studio.js'):
        shutil.copyfile(SOURCE / 'styles/swiss-grid' / name, project / name)
    # Avoid network dependence inside Chromium for this runtime proof. The test
    # uses Liberation Sans/Arial; customer pieces retain their selected font.
    html = (project / 'index.html').read_text()
    html = '\n'.join(line for line in html.splitlines() if 'fonts.googleapis.com' not in line)
    html = html.replace("'Inter', sans-serif", "'Liberation Sans', Arial, sans-serif")
    html = html.replace('https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js', 'gsap.min.js')
    (project / 'index.html').write_text(html)
    shutil.copyfile(ROOT / 'cloud/node_modules/gsap/dist/gsap.min.js', project / 'gsap.min.js')
    run(HF, 'snapshot', project, '--at', '0.6,3.6,6.6', '--no-end', '-o', OUT / 'stills')
    video = OUT / 'cloud-motion-smoke.mp4'
    started = time.monotonic()
    run(HF, 'render', project, '-o', video, '-q', 'high', '-w', '2', '--quiet')
    elapsed = round(time.monotonic() - started, 2)
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=codec_name,width,height,avg_frame_rate,nb_frames:format=duration',
        '-of', 'json', str(video)], text=True))
    stream = probe['streams'][0]
    assert (stream['width'], stream['height']) == (1920, 1080), probe
    assert stream['codec_name'] == 'h264', probe
    assert stream['avg_frame_rate'] == '30/1', probe
    assert abs(float(probe['format']['duration']) - 9) < 0.1, probe
    run('ffmpeg', '-v', 'error', '-xerror', '-i', video, '-f', 'null', '-')
    # Source is a loop: verify seam and pacing from the encoded pixels. Keep all
    # reports when a check fails rather than claiming the output passed.
    checks = {}
    for name, args in (
        ('pacing', [sys.executable, str(SOURCE / 'scripts/pacing_check.py'), str(video), '--loop']),
        ('loop', [sys.executable, str(SOURCE / 'scripts/loop_check.py'), str(video)]),
    ):
        checks[name] = subprocess.run(args, timeout=120).returncode == 0
    receipt = {
        'upstream_commit': '18891e4996abb7ccc0085f2d43cef2fd7eff1dc8',
        'hyperframes_version': '0.8.181', 'render_seconds': elapsed,
        'bytes': video.stat().st_size, 'sha256': hashlib.sha256(video.read_bytes()).hexdigest(),
        'metadata': probe, 'decode_pass': True, 'checks': checks,
        'pass': all(checks.values()),
        'scope': 'Runtime proof with a system font; no account upload or iPhone placement tested.',
    }
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
    if not receipt['pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
