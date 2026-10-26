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
libraries and HyperFrames' managed browser. Paste the contents of
`cloud/bootstrap.sh` into the dedicated cloud environment's setup script: that
stage does not necessarily start in the checkout directory. It locates the
checkout, or defers installation until the session if the checkout is not yet
available. It starts no server and requires no
model API key. The smoke test makes a 9-second 1080p H.264 loop from the pinned
upstream Swiss Grid reference, with GSAP served from the project. It requests a
system-font fallback, but HyperFrames still fetches and injects Inter; this is not
an offline-rendering test. It records actual render time, metadata,
decode checks, pixel pacing and loop checks under `output/cloud-motion-smoke/`.
Keep the MP4, stills, contact sheet and receipt together. Inspect the images as
well as the exit code. This runtime proof does not validate every style
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

## October 26, 2026 cloud acceptance

Environment: **Megaphone motion pilot**, restricted networking plus package
registries, no environment secrets. The first session failed before Claude
started because setup was launched outside the checkout. The corrected bootstrap
located `/home/user/megaphone-claude-plugin`, installed dependencies and cached
Chromium. The next session rendered successfully without source repairs:
[cloud test and downloadable outputs](https://claude.ai/code/session_01W6LBYAUJA2coYhstsegeWt).

At source commit `9b69b4aa0b72575f510940bffe9887a44ca5be7e`, Node 22.22.0 and
Chromium 152 rendered the 9-second reference in **16.78 seconds**, using two
workers and software rendering. Whole smoke command: 26.5 seconds. Output:
1920×1080, H.264 High/yuv420p, 30 fps, 270 frames, no audio, 224,721 bytes.
SHA-256: `c102a4c83598f729ab09fd8ee8fe104a11df1e999c3f71bbce9ac181f75502ff`.
Full decode, pacing (longest gap 0.9 s) and encoded-loop seam checks passed.
The local task downloaded the cloud MP4, independently verified its size/hash
and decoded it, and inspected an extracted contact sheet. No Vercel render was
used. Matching phone/server source is prepared; live trigger/upload/placement
acceptance remains pending activation and the account's motion permission.

## Connect the phone after the reviewed app/server rollout

1. Reconnect the existing Megaphone connector and review its **motion graphics**
   permission. Old connector grants keep their original scope until you approve
   the new one. Do not create a second Megaphone account or connector.
2. Create a dedicated **API-only** Claude cloud routine, with this repository
   on main, the **Megaphone motion pilot** environment and the instructions in
   `cloud/motion-routine.md`. Include only the Megaphone connector. No schedule,
   sales routine or unrelated connectors are needed.
3. Generate the routine's scoped API token in Claude. Store its Fire URL and
   token in Megaphone's **B-roll from Claude → Connect Claude cloud** form.
   The form keeps them in this iPhone's Keychain for the current Megaphone UID.
   Never paste the token into chat or a Git repository.
4. In a recording, select a motion style and tap **Add motion graphics**. The
   phone queues the sections and fires that routine once with only the job ID,
   video key and style. After acceptance the computer can be closed. Return to
   the same recording and tap **Place B-roll** when the graphics are ready.

The first version reports readiness when the editor is reopened; no new push
notification is implemented. If Claude's usage allowance or token is rejected,
check the cloud run and cancel the saved pending job before explicitly trying
again. Never automatically retry an uncertain trigger. The separate local Mac
B-roll flow remains available.
