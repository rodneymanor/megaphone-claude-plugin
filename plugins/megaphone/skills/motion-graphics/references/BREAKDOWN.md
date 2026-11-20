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

## Pop-ups

A pop-up is a small card under the captions that pops in on a spoken word (MegaphoneApp PROJ-889..891,
server PROJ-892). The phone draws it; the plan sends only words. Contract: MegaphoneApp
`docs/plans/2026-11-20-widget-kit.md`, "The plan field `popup`".
- `popup` on a section: null (most sections), or
  `{"kind": "stat", "words": ["views"], "label": "views", "title": null, "sub": null, "value": "300K", "icon": null, "items": []}`.
  Each kind needs the fields it lists below. Leave the rest null, and `items` [].
- Where: only on a plain `face` section (no card, top, sticker, mark or shrink). Never section 1 (the hook)
  or the last section (the CTA). One at a time: between two pop-ups, at least one face rest (a plain `face`
  section with no pop-up). A `full`, card or shrink section between them is not a rest.
- On screen 1.5–4 s: only on a section of at least 1.5 s. The phone ends it at the section end, at most 4 s.
- Use one only when the line has a clear thing to show. Match the moment:
  - a number said → `delta` (it went up), `stat` (one number), `count` (a number of things);
  - an amount or price → `price`, or `prices` for three; three numbers → `stats`;
  - a do and a don't → `rules`; a choice of two actions → `buttons`;
  - a choice of tools → `chips`, or `pair` for two used together; one tool or app named → `app`;
  - steps of one process in one line → `steps`;
  - a before and after → `compare`, `slider`, `gauge` or `tracks`;
  - a message that comes in → `alert`; a day → `day`; how much is used → `usage`;
  - posts or videos in a row → `phones`; editing → `timeline`; things named in a row → `icons`.
- `words`: 1–4 single words of the section's text, as spoken, in spoken order. `words[0]` is the key word:
  it pops the card in. Each later word starts the card's next move.
- `label` ≤ 3 words, `title` ≤ 4, `sub` ≤ 6, an item `name` ≤ 4. Words of the section's text or `caption`; you may
  change a word's form ("post" → "posted"). Never a new name, number or claim.
- `value`: a number or amount exactly as the section says it ("300K", "$200", "22%", "7 min", "×2"). Write
  numbers as digits ("7 min", not "seven min"): the phone counts digits up. The same number, the same %, the
  same currency and unit as that one spoken amount ("200 dollars for 50 videos": "$200" or "50 videos", never
  "$50"). Never made up, never rounded. No number said → no `value` kind. A number in a `label`, `title`,
  `sub` or item `name` follows the same rule.
- `icon`: one of `chart, money, time, content, camera, video, chat, user, users, check, cross, up, down, star,
  heart, fire, bolt, book, tag, gift, target, loop, lock, mail, phone, code, spark, megaphone, calendar, bell,
  eye, idea`, or null. The phone draws its own plain glyph. No real logos.
- The kinds (fields; what it shows; its moves):
  - `app` (`icon`, `title`, `sub`): an icon tile, a name, one line. For one tool the line names.
  - `alert` (`title` who, `sub` the message): a phone alert with "now". `words[1]` adds a green check.
  - `buttons` (`title` the accent button, `sub` the dark button): two actions. `words[1]` presses.
  - `delta` (`value`, `sub`, `label` under a small clip of this video): a green ↑ number and a word. It counts
    up on `words[0]`. Only for a number that went up.
  - `price` (`value`): one amount on an accent pill.
  - `pair` (2 items: `name`, `icon`): two name pills with "+". `words[1]` adds the second pill.
  - `day` (`label` the day, `value`, `sub`): a white square with a day, a big value and a word.
  - `stat` (`label`, `value`): a white tile with a small label and one big value. It counts up on `words[0]`.
  - `gauge` (`sub`): a dial from green to red, a word under it. `words[1]` swings the needle to red.
  - `slider` (`label`, `sub` before, `title` after): a slider that moves on `words[1]`, red to green.
  - `usage` (`icon`, `label`, `value` a %): a bar that fills on `words[0]`.
  - `compare` (2 items: `name`, `value`): two labelled bars. `value` is a relative size only ("1", "3"), never
    shown, so it need not be said. `words[1]` grows the second bar green.
  - `steps` (2–4 items: `name` the step): numbered circles. `words[i]` fills circle i.
  - `rules` (2 items: `name`, `ok`): a green "do" pill (`ok: true`) and a red "don't" pill (`ok: false`).
    `words[i]` slides pill i in.
  - `chips` (2–3 items: `name`, `icon`): white tiles, an icon and a word each. `words[i]` pops tile i.
  - `phones` (3–5 items: `name`): phone tiles with a label. Checks pop one by one from `words[1]`.
  - `tracks` (`title` before, `sub` after): 4 edit tracks, busy red to clean green on `words[1]`.
  - `timeline` (no fields): 3 coloured lanes and a running playhead.
  - `count` (`value`, `title`, 2–4 items: `name`): a big number and a word, a tile grid, then pills. `words[0]`
    counts, `words[1]` adds the tile.
  - `stats` (`title`, 3 items: `name`, `value`): 3 stat boxes and a line chart. `words[0]` counts up.
  - `prices` (3 items: `name`, `value`): 3 price cards. `words[i]` brings card i.
  - `icons` (2–3 items: `icon`): app-style tiles beside the head. `words[i]` brings tile i.

## Not yet

- `shot` cards (a real screenshot in a white card) work on the phone, but the job server accepts only
  `mb-`, `mo-`, `gs-` and `plan-` files. Until it accepts `shot-<set>-NN.png`, use a green screen for proof.
