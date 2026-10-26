# Shared edit rules: candidate handoff — 2026-10-26

These are validation candidates for the existing Megaphone B-roll workflow.
No candidate is registered as a second engine or deployed as a second routine.
Production Mac/cloud instructions and in-flight jobs are unchanged.

- `megaphone-broll.md`: complete Mac engine candidate based on the current local
  v10 engine, preserving its creator styles, overlays, green screens and truth
  checks. Candidate v11 replaces cadence alternation/quotas with the shared rules.
  It lives outside all watched/installed engine directories.
- `motion-routine.md`: complete cloud routine candidate. It preserves the
  existing authenticated job claim, progress, packaging and upload contracts.
- `HISTORICAL-BASELINE.md`: read-only results on seven old plan files. No source
  export was available, so these are diagnostics, not delivery approvals.

Policy: `plugins/megaphone/skills/motion-graphics/references/edit-rules.json`.
Instructions: `EDIT-RULES.md` beside it. Checker: `cloud/plan_check.py`.
The app bundles byte-identical `MegaphoneApp/Resources/EditRules.json` offline.

## Checks already run

`python3 -m unittest discover -s cloud/tests -v`: 14 tests passed, including policy
parity with the sibling app checkout, changed IDs/times/words, unsupported input,
nonfinite times, overlap, continuous full graphics, final tags/layout/duration,
and a nonzero diagnostic-only exit when source verification is missing,
missing files/gates and same-layout visual changes. Python syntax compilation
passed. No model call, render, upload, job claim or runtime cutover was performed.

## Next acceptance pass

Run one explicitly selected candidate job per route, with different job IDs.
Each job keeps its selected route for all repairs/retries; a failure never starts
the other renderer. Capture unchanged source-sections.txt, plan.json, both checker
receipts and media gate output. Validate actual placement in the phone, then
check failure/retry and one-use delivery behavior. Required FAIL must produce no
Mac Ready marker or cloud upload/finish calls. Use no public posting/customer messages.

## Cutover after both routes pass

1. Compare this candidate's preserved style/content instructions with any newer
   Mac/cloud source changes; retain unrelated work. Freeze new job dispatch briefly
   using the existing operator controls; let in-flight jobs finish before replacement.
2. Replace the existing Mac engine source and its installed
   `~/Baton/engines/megaphone-broll.md` with the verified candidate; retain its
   original filename/engine identity. Follow the existing engine-install bookkeeping.
3. Replace `cloud/motion-routine.md` with the verified cloud candidate and update
   the existing deployed routine's prompt through its normal release path. Update
   the skill's normal Create step 3 to read EDIT-RULES.md and run plan_check.py;
   remove the now-obsolete default-split/cadence and candidate-only guidance.
4. Verify both active instruction copies and the policy digest, then resume job
   dispatch. Confirm one planner per job, and archive these candidate instructions
   after recording the accepted versions. Retain historical plans as evidence.

The cutover is intentionally pending the user's later test pass. Do not copy the
candidate beside the installed engine under another name: that would register a
second engine. Do not activate one route's new rules while claiming both migrated.

## Failure evidence and recovery

- Pre-render FAIL: source/plan/checker report. Repair at most twice; stop without
  rendering after a remaining required failure.
- Post-render FAIL: final plan, tags, file inventory and gates. Do not upload.
- Delivery ambiguity: preserve job ID/state and stop; do not replay/fall back.
- Wrong phone placement: original section export, delivered tag, expected and
  actual composition interval; keep the saved draft and use Undo.

Revert the shared-rule implementation snapshot for code rollback. Once cut over,
restore both previous active instruction versions together after in-flight jobs
finish. Never reset/force-push or discard unrelated source/runtime work.
