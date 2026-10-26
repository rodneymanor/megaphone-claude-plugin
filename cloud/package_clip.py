"""Tag a verified opaque motion clip for the existing Megaphone phone placer.

Example: python3 cloud/package_clip.py scene.mp4 output/clips --video-key a1b2c3d4
  --section-id SECTION --text 'Exact section words' --n 1 --of 3 --duration 3.5
Prints the {name, bytes} packet used by the authenticated MCP upload/finish tools.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--video-key', required=True)
    parser.add_argument('--section-id', required=True)
    parser.add_argument('--text', required=True)
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--of', type=int, required=True)
    parser.add_argument('--duration', type=float, required=True)
    parser.add_argument('--place', choices=['split', 'full'], default='split')
    args = parser.parse_args()
    if not re.fullmatch('[a-z0-9]{1,8}', args.video_key):
        parser.error('Use the exact video key returned by the motion job.')
    if not 1 <= args.n <= args.of <= 40 or not 0 < args.duration <= 120:
        parser.error('Use 1..40 clips and a positive section duration up to 120 seconds.')
    if not args.section_id.strip() or not args.text.strip():
        parser.error('Preserve the exact section ID and words from the job.')
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=codec_name,avg_frame_rate:format=duration', '-of', 'json', str(args.source)], text=True))
    stream = probe['streams'][0]
    if stream['codec_name'] != 'h264' or stream['avg_frame_rate'] != '30/1':
        parser.error('The pilot accepts opaque H.264 at 30 fps; no alpha remuxing.')
    if abs(float(probe['format']['duration']) - args.duration) > 0.1:
        parser.error('Retiming is required: clip duration must match this section within 0.1 seconds.')
    tag = dict(v=1, set=f'motion-{args.video_key}', n=args.n, of=args.of,
               section=args.section_id, text=args.text, place=args.place)
    args.destination.mkdir(parents=True, exist_ok=True)
    target = args.destination / f'mb-{tag["set"]}-{args.n:02d}of{args.of:02d}.mp4'
    if target.exists():
        parser.error('Preserving an existing clip; choose a fresh destination.')
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-i', str(args.source), '-map', '0:v:0',
                    '-c', 'copy', '-metadata', 'comment=' + json.dumps(tag, separators=(',', ':')),
                    '-movflags', '+faststart', str(target)], check=True, timeout=120)
    saved = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
        'format_tags=comment', '-of', 'json', str(target)], text=True))
    if json.loads(saved['format']['tags']['comment']) != tag:
        raise SystemExit('Tag verification failed. Do not upload this file.')
    if target.stat().st_size > 200 * 1024 * 1024:
        raise SystemExit('Clip exceeds the existing 200 MB limit. Do not upload it.')
    print(json.dumps({'name': target.name, 'bytes': target.stat().st_size}))


if __name__ == '__main__':
    main()
