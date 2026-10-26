# One Megaphone B-roll workflow

The numeric authority is `edit-rules.json` beside this file. The phone bundles an
identical copy for offline use. This policy extends the existing job, renderer,
clip tags and phone placement. Each job uses only its requested Mac or cloud
route, including retries. Never fall back to the other route automatically.

Preserve every supplied section ID, text and time. The phone places tagged clips
within one section, bounded by available footage. Do not merge IDs or pretend a
longer JSON range makes a graphic span sections. A short section can remain face.

Choose layouts from meaning: proof uses real supplied footage/pages, a number
uses its actual figure, a concept gets a simple graphic, and camera/rest beats
can stay face. Prefer a split proof opening and a face CTA when appropriate.
Honor the creator's style, brand and technical renderer constraints. Never
invent proof, quotes, figures, logos or endorsements to satisfy cadence.

Required machine checks: valid complete plan matching the input; no continuous
full-graphic run above maximumFaceAbsence. Consecutive full clips count together.
Warnings: short/long shots, median, face-only/full shares and visual switch rate.
There is no cap on total camera-visible share. Changing the graphic counts as a
shot even if layout stays split. A continued view is not a new shot solely
because a section changes. Preferences reflect research, not proven view lift.

Keep designed motion calm: at most three animations in the opening five seconds,
at most two new elements in half a second, then hold. Inspect this in the existing
stills/contact-sheet checks; section JSON cannot verify animation events.
A zoom or same-layout graphic switch does not certify a concealed camera cut.

Write `source-sections.txt` from the exact input sections (no rewriting), and
`plan.json` with v=4 and all sections, including face/rest. Each section has id,
start, end, text, layout and clip/image when applicable. Mac supports face,
split, full, overlay and greenscreen; cloud supports face, split and full only.
Use the selected route when checking:

    python3 cloud/plan_check.py PLAN --source SOURCE --route cloud

The Mac uses the absolute plugin checkout path for this command and `--route mac`.
Check before render. Allow at most two repair passes after the initial plan.
A required FAIL stops the job; warnings do not trigger endless repairs. After
clip gates, update dropped sections to face, then run the same command with
`--final` before any upload or `Ready:` output. It checks actual media tags and
available duration too. Never deliver on a required failure. Preserve output as
`plan-check-before.txt` and `plan-check-final.txt` using the session's file tools.

The Mac cadence alternation/quotas and cloud default-split planning instruction
are superseded by this policy only after the documented verification cutover.
Before that, use these instructions in explicitly requested candidate test jobs.
Do not run both planners for one job. Existing in-flight jobs retain their rules.
