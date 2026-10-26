# Claude cloud motion pilot

The existing plugin owns Claude's Megaphone account connection. The iPhone's
`BrollJobService` and backend `broll-jobs.ts` currently own the job queue, which
requires a paired-Mac claimant; the hosted MCP has no media job/upload tools.
Consequently a new skill alone cannot turn the current Mac button into a cloud
trigger. First prove rendering in Claude cloud, then extend that existing queue
and authenticated connection rather than adding a second job store.

## Run the bounded proof

Select `rodneymanor/megaphone-claude-plugin` in a **Cloud** Claude Code session.
Run from the repository root:

```sh
bash cloud/setup.sh
python3 cloud/smoke.py
```

The setup installs the locked Node dependencies, FFmpeg, Chromium's Linux
libraries and HyperFrames' managed browser. It belongs in a dedicated cloud
environment's setup script once validated. It starts no server and requires no
model API key. The smoke test makes a 9-second 1080p H.264 loop from the pinned
upstream Swiss Grid reference, with GSAP served from the project and a system
font to isolate browser/network issues. It records actual render time, metadata,
decode checks, pixel pacing and loop checks under `output/cloud-motion-smoke/`.
Keep the MP4, stills, contact sheet and receipt together. Inspect the images as
well as the exit code. A system-font runtime proof does not validate every style
or customer fonts, media, portrait layout, uploads, notifications or placement.

For a fresh rerun, supply a new output directory; never delete an existing result.
Use at most two render workers. Keep the test on synthetic content; no uploads,
customer data, paid AI clips or account writes are needed. A one-off cloud render
must not run the sales or daily-content routines. No subagents.

## Minimal scope and next integration

- The new skill is the customer workflow. Its bundled upstream files preserve
  the requested styles, templates and real verification scripts, with the MIT
  license and exact source commit. Gallery videos are omitted to keep the plugin
  small and avoid a localhost UI in cloud sessions.
- `package.json`/lock, `setup.sh` and `smoke.py` are the reproducible execution
  environment and the test of the requested renderer. No new hosting dependency,
  Vercel renderer, persistent credential or customer data store is introduced.
- The existing plugin version remains 0.2.0 until the pilot passes and the
  customer trigger/delivery contract is implemented. Do not describe this as an
  automatic phone feature yet.
- After cloud acceptance, wire an explicit phone request to a user-authorized
  Claude routine trigger; have it use the same account's job claim/upload/result
  operations. Keep credentials private, preserve the local B-roll route, and
  return the result through the existing phone placement workflow. Missing cloud
  connection or usage exhaustion must be visible, not a silent Mac fallback.

Official references: [Claude cloud environments](https://code.claude.com/docs/en/cloud-environments),
[API-triggered cloud tasks](https://code.claude.com/docs/en/routines#add-an-api-trigger),
[source skill](https://github.com/ItsssssJack/claude-video-2/tree/18891e4996abb7ccc0085f2d43cef2fd7eff1dc8).
