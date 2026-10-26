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
