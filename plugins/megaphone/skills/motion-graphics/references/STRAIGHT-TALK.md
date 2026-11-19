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
  `clip`, `poster`, `scene` and `n` are null.
- `zoom`: `jump` or null. On most line changes the shot jumps in, then back out: `jump` on one section,
  null on the next, and so on. **null on section 1** (the hook). The `pill` line always has `jump`, and
  the section just before it is null (wide), so the pill line jumps in from a wide shot.
- `emphasis`: 0–1 word, on about half the sections: the word the line turns on ("tool", "rich", "problem").
  The phone paints it yellow, at the caption's size.
- `hookCard`: line 1 is 3–6 words that state the hook (`size` `medium` or `large`), lowercase; fewer only
  when the spoken hook (section 1) is shorter. An optional line 2 in `size` `small` adds a short aside
  ("(or waste thousands)"). Line 1 is words in a row from section 1 (the spoken hook), as said; never
  drop a "not" or "never" just before them. Line 2 uses words the creator said in the video.
- `pill`: `true` on the one section that is the video's main question or rule ("What problem should I use
  AI to solve?"). **At most 1 `pill` per video**, never section 1. The phone shows that line on a white
  pill that builds word by word, in place of its captions. A video with no clear main question or
  rule has no pill.
- `caption`: null, unless speech-to-text clearly misheard a word, or to mask a swear word ("f*cking").
  Then it is the line with that fix, word for word: the same number of words in the same order (the
  phone puts each caption word on a spoken word's time). Never change a "not" or "n't", a number or
  an amount ("fifteen", "-5%"). No other words on screen: the captions are the creator's words.
- `transition`: null. `sound`: null (the look has no sound effects).
- Cadence: something changes every 2–4 s, through the zooms. EDIT-RULES.md's card and shot shares do not
  apply: this look has no cards.
- Pass 2: skip all steps except step 7, step 10 and the final check. An edit with no files at all is
  fine: the phone draws the plan alone.

## Not yet

- A red key word for one bad word ("useless"). It needs a second colour on the phone. All key words are yellow.
- App logo stickers. The truth rules do not allow real logos yet.
