# Claude cloud motion pilot

The existing plugin owns Claude's Megaphone account connection. The iPhone's
`BrollJobService` and backend `broll-jobs.ts` own the job queue. Before this pilot,
that queue required a paired Mac and the hosted MCP exposed no media job tools.
The deployed motion permission now extends that same queue and connection;
there is no second job store. Phone installation and placement acceptance remain
separate from server deployment.

## Current mobile trigger — replaces the URL/token form

The phone now queues this recording's existing motion job and opens Claude Code
with `repo`, `branch`, `mode` and an exact-job prompt prefilled. The creator taps
**Send** in Claude, using the existing Megaphone MCP connector. The session
claims that job, renders and uploads through MCP. Return to the original phone
recording and tap **Place B-roll**. The phone never requests or stores a new
routine URL/token, and it does not call the routine-fire API.

The app's **Open Claude** action reopens the same queued job. Its style is retained
in the existing server-owned section export; no second job/style store is added.
An opened composer is not a running render: the job stays queued until MCP claims
it. If the link cannot open, the queued job remains available to reopen or cancel.
A working job cannot open another new render session. The server still rejects a
second claim, including two composers opened before the first claim completes.

Cloud handler: `cloud/motion-handoff.md`. Claude Code access and the existing
connected Megaphone tools (including motion permission) must be available in the
selected cloud environment. Existing GitHub/cloud-environment access is still
needed for this renderer. No phone token setup is a substitute for those checks.

The API-only pilot described below is historical. Its URL/token setup is
superseded for new mobile jobs; do not follow those old phone-connection steps.
Existing in-flight API runs and the edit-rule acceptance/cutover are separate.
Do not revoke an existing run's credential or activate a candidate as part of
this source change. No new scheduled poller, dispatcher or renderer is created.

Official mobile handoff: https://support.claude.com/en/articles/14898120-open-the-claude-mobile-app-with-a-link

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
- The existing plugin version remains 0.2.0 during the owner pilot. A customer
  release still requires updated-phone installation and placement acceptance.
  Do not describe installing the skill as automatic phone activation.
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

## Historical API-only pilot setup (superseded for the phone)

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

## October 26 production activation and live handoff

Backend commit `a43e8a38e` is deployed to `www.gencapp.pro`
(`dpl_EcwvGCLyWfFk7uNYheeK8GE6qPBV`). The matching hosted MCP is deployed
(`dpl_UdvEovuZ4oFWrMGhdxfc6JYCEeRv`) and served through
`joinmegaphone.com/mcp`. Public discovery advertises `megaphone:motion`;
unauthenticated MCP access returns 401. A temporary read/motion acceptance grant
verified account identity, all four motion tools, rejection of a missing-job
claim, a live motion-queue read and denied direct Firestore authorization-record
access. The temporary grant was revoked after the checks.

The owner's existing Claude Megaphone connector was reauthorized with the motion
permission; its same connector ID now exposes 28 tools. The dedicated
[Megaphone motion graphics routine](https://claude.ai/code/routines/trig_01EzpsLU9yz68Mo44WjXuLQX)
is active with only an API trigger and the Megaphone connector. Its scoped token
is stored privately outside the repositories. The restricted cloud environment
also permits the existing upload host `ny-s3.storage.bunnycdn.com`.

One synthetic, nine-second job proved API fire → exact-job claim → cloud render
→ storage upload → server-verified `sent` state, without another API fire:
[completed run](https://claude.ai/code/session_0165sK79yXA1aRAf1LrkNLJ7).
Job `hwP6FmAeqKLvqKS9suPD`, video `dpl26abc`, was created at 17:05:33.490 UTC
and marked sent at 17:07:06.967 UTC (about 93.5 seconds). Its MP4 is 224,593 bytes,
1920×1080 H.264, 30 fps, 270 frames and 9 seconds. The task independently
downloaded it, verified its byte count, fully decoded it and read back the exact
section ID/text and `place: split` metadata. SHA-256:
`82ec597637a8e3202a235f1f2fae6efb5ea8d07ee919b0d2523d4ec6c5dd104d`.
Proof and the returned MP4 are retained in the ignored
`output/cloud-acceptance-2026-10-26/` folder. This confirms cloud delivery, not
physical iPhone placement. The updated phone build now uses the MCP handoff above; its physical-phone
handoff/Send/placement/export acceptance remains pending.
