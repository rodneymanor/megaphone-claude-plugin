# Straight Talk look (`style=straight-talk`)

One copy of the Straight Talk rules. Megaphone's server makes the plan from this file (Gen-C-A
`scripts/sync-breakdown-rules.mjs` copies it). MegaphoneApp tickets: PROJ-864 (the look), PROJ-865 (the
server plan), PROJ-866 (`pill`). Reference: Instagram reel Df0YcKxGtns. Plan:
MegaphoneApp `docs/plans/2026-11-18-straight-talk-look.md`.

A face-only look. The speaker stays full screen for the whole video. The edit is small white captions,
yellow key words, jump zooms, a white hook pill and one key line on a white pill.
**The phone draws every word and move.** You write `plan.json` only: no `mb-`, no `mo-`, no
`look-card.mjs`, no scenes, no green screens. Pass 1 holds with these changes:
- `plan.json` gets `"style": "straight-talk"` (small white captions at the chest, yellow key words at the
  caption's size, a white hook pill, no colour look).
- Every section is `face`. No `card`, `top`, `sticker`, `mark`, `split`, `full`, `shrink`, `greenscreen` or `overlay`.
  `clip`, `poster`, `scene` and `n` are null. The one card is a `popup` (Pop-ups, below).
- `zoom`: `jump` or null. On most line changes the shot jumps in, then back out: `jump` on one section,
  null on the next, and so on. **null on section 1** (the hook). The `pill` line always has `jump`, and
  the section just before it is null (wide), so the pill line jumps in from a wide shot.
- `emphasis`: 0–1 word, on about half the sections: the word the line turns on ("tool", "rich", "problem").
  The phone paints it yellow, at the caption's size.
- `hookCard`: line 1 is 3–6 words that state the hook (`size` `medium` or `large`), lowercase; fewer only
  when the spoken hook (section 1) is shorter. An optional line 2 in `size` `small` adds a short aside
  ("(or waste thousands)"). Line 1 is words in a row from section 1 (the spoken hook), as said. Line 2
  is words in a row from one section, as said. A line keeps the claim as the creator meant it: never
  start after a "not" or "never" in that line, keep a whole amount ("one hundred and fifty dollars")
  and any condition that limits the claim ("until the trial ends"), and never turn a question the
  creator answers "no" into a statement. No line fits: no hook card (`"lines": []`).
- `pill`: `true` on the one section that is the video's main question or rule ("What problem should I use
  AI to solve?"). **At most 1 `pill` per video**, never section 1. The phone shows that line on a white
  pill that builds word by word, in place of its captions. A video with no clear main question or
  rule has no pill.
- `caption`: null, unless speech-to-text clearly misheard a word, or to mask a swear word ("f*cking").
  Then it is the line with that fix, word for word: the same number of words in the same order (the
  phone puts each caption word on a spoken word's time). Never change a "not" or "n't", a number, an
  amount or its unit ("fifteen dollars", "-5%"), and never move words. Mask swear words only. No other words on screen but a pop-up's: the captions and pop-ups are the creator's words.
- `transition`: null. `sound`: null (the look has no sound effects).
- Cadence: something changes every 2–4 s, through the zooms. EDIT-RULES.md's card and shot shares do not
  apply: this look has no split or full cards.
- Pass 2: skip all steps except step 7, step 10 and the final check. An edit with no files at all is
  fine: the phone draws the plan alone.

## Pop-ups

A pop-up is a small card under the captions that pops in on a spoken word (MegaphoneApp PROJ-889..891,
server PROJ-892). The phone draws it; the plan sends only words. Contract: MegaphoneApp
`docs/plans/2026-11-20-widget-kit.md`, "The plan field `popup`".
- `popup` on a section: null (most sections), or
  `{"kind": "stat", "words": ["views"], "label": "views", "title": null, "sub": null, "value": "300K", "icon": null, "items": []}`.
  Each kind needs the fields it lists below. Leave the rest null, and `items` [].
- Where: any section but section 1 (the hook) and the last section (the CTA). One at a time: a section
  with no pop-up between two pop-ups.
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
- `value`: a number or amount exactly as the section says it ("300K", "$200", "22%", "7 min", "×2"). The same
  number, the same %, the same currency. Never made up, never rounded. No number said → no `value` kind.
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

- A red key word for one bad word ("useless"). It needs a second colour on the phone. All key words are yellow.
- App logo stickers. The truth rules do not allow real logos yet.
