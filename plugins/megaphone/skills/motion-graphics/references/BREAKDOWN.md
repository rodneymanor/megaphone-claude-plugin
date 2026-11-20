# Breakdown look (`style=breakdown`)

One copy of the Breakdown rules. The Mac engine (`megaphone-broll.md`) and the link flow (`link.md`, PROJ-841)
both read this file. MegaphoneApp tickets: PROJ-844 (parent), PROJ-845..850. Source edits and values:
`/Volumes/The Vault/Content/reel-edits/2026-11-17-megaphone-lane-v1/LANE.md`.

Split screens and simple cards that explain the point (MegaphoneApp PROJ-844).
**The phone draws every card, word and move.** You write `plan.json` only: no `mb-`, no `mo-`, no
`look-card.mjs`, no scenes. Pass 1 holds with these changes:
- `plan.json` gets `"style": "breakdown"` (small white captions, a white hook card, no colour look).
- Each section's `layout` is one of:
  - `face`: the default, for the hook, turns and the CTA. **The last section is always `face`** (never end
    inside a shrink, a split or a full card).
  - `split`: a `card` on the top half, the speaker on the bottom half. For a claim, a choice, or the state of a
    thing the line names. `clip`, `poster`, `scene` and `n` are null; `gate` is `"pass"`.
  - `full`: a `bars` card only (a comparison the line makes). At most 1 per video, at most 4 s.
  - `shrink`: the speaker shrinks into a box on black. For a punch line or a "no" ("I don't believe in…",
    "they just make you guess"). At most 2 per video, never section 1, never two in a row. Optional, with a
    `top`: `"mark": "strike"` (a red line through it). No red ring around the box (retired, PROJ-885).
  - `greenscreen`: proof from a real public page (rules under Green screen; Pass 2 step 6b). At most 2.
  - No `overlay`.
- `card` (split, full, and a sticker on face), one of these kinds. **Words:** every word on a card is a word of the
  section's text or `caption`; you may change a word's form ("reject" → "rejected") and add "?" to anything
  that guesses. Never a name, number or claim the line does not say. A card shows an idea, never proof.
  - `{"kind": "option", "label": "Option 1", "title": "hacked?"}`: one choice of two or three; `title` 1–2 words.
  - `{"kind": "status", "title": "System status", "rows": [{"name": "App Store Connect", "ok": false, "note": "outage?"},
    {"name": "TestFlight"}]}`: **2–4 rows** of things the line (or the video) names: real names, never stand-ins
    like "your app" or "scans". `ok: false` paints the dot red (the point); `note` 0–1 words that say the state
    ("down?", "rejected"), never a verb from the line ("run"). One thing alone → use `message` instead (except step 1 of a growing list, below).
    `title` may be a plain label ("Status").
  - `{"kind": "message", "label": "App Review", "title": "Submission rejected"}`: a notice the line describes;
    `label` is who sends it (named in the video), `title` 1–3 words that state the notice, not a question.
    The phone draws grey lines for the body. **At most 1 `message` card per video**, never two in a row.
  - **Steps of one process** ("a ticket comes in, a model analyzes it, sends the code, you merge it"): one
    `status` list that grows, never one card per step. Each step's section is a `split` with the same `title`
    and the rows so far: step 1 shows row 1, step 2 shows rows 1–2, and so on (2–4 steps). The newest row is
    the point (`ok: false`, no `note`); earlier rows are `ok: true`. Back-to-back panels cut in (no drop), so the list
    grows from card to card. `sound`: `whoosh` on the first step only, then `pop`.
  - `{"kind": "bars", "title": "Time it takes", "label": "9 out of 10 times", "bars": [{"label": "Build the app",
    "value": 1}, {"label": "Get accepted", "value": 4, "point": true}]}`: 2–3 bars; a value is only a length
    (never shown as a number); `label` only with a number the line says. **Any "longer / more / faster than"
    comparison is a `full` bars section**, not a message card. The phone grows the bars after 0.35 s.
- `sticker` (any section, best on a `split`): one word, or a word and "?", from the line ("why?"), on a red pill.
  On a split it sits on the card's panel; on a face section, beside the face. Add `word` (the spoken word it
  pops on). At most 2 per video. Not a `card` kind any more.
- `top` (face or shrink sections, never split): one word or a phrase of 2–3 words from the section's text,
  lowercase, for a turn ("my advice", "9 out of 10", "conspiracies"). At most one every 8 s. Add `word`: the
  spoken word it pops on (one word of the text).
- `zoom`: face sections only. `punch` on a face section that follows a split, full or shrink; `punchIn` on a
  short, hard line; null on the CTA. Never on every face section. null on split, full and shrink.
- `transition`: null (the phone cuts panels in and pops words).
- `sound`: `whoosh` on split and full sections; `pop` on a section with a `top` or a sticker; null on a plain
  face section. The phone adds the shrink's whoosh, the bars' riser and a mark's click by itself.
- `emphasis`: 0–1 word, on at most every other section (red caption words lose their punch when common).
- `hookCard`: 1–2 lines, 2–4 words each, as usual (lowercase). Each line shows on a white pill.
- Cadence: EDIT-RULES.md holds. Something changes every 2–4 s; split and shrink keep the speaker on screen.
- Pass 2: skip steps 1–6 and 8–9. Only green screens (step 6b), then step 7, step 10 and the final check.
  An edit with no files at all is fine: Megaphone IQ sends the plan alone and the phone draws it.

## Not yet

- `shot` cards (a real screenshot in a white card) work on the phone, but the job server accepts only
  `mb-`, `mo-`, `gs-` and `plan-` files. Until it accepts `shot-<set>-NN.png`, use a green screen for proof.
