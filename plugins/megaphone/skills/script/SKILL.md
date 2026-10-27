---
name: script
description: Get one Megaphone script written and saved in the customer's custom voice, then offer to read it, make it stronger, see what it's built on, or try a new angle. Use for a Megaphone script, hooks for an idea, or when the customer asks to write a script with Megaphone.
---

# Megaphone Script

Use the Megaphone connector bundled with this plugin. First call `megaphone_account`, `megaphone_content_context`, and `megaphone_list_voices`, even when the customer invokes this skill directly. If the connector or a required tool lacks permission, direct them to **Customize > Plugins > Megaphone > Connectors** to reconnect and approve access on their phone. Never ask for credentials or add a second connector.

If onboarding is incomplete, run the Megaphone Setup flow for only the missing areas and resume here after a fresh `megaphone_content_context` says `complete`. Require a ready synced *custom* voice. With none, ask the customer to finish one in the updated Megaphone iPhone app and sync it. With several, ask which voice to use; remember that choice only for this conversation. Do not substitute a preset or the experimental iPhone creator brief.

**Megaphone writes every word.** Never write, rewrite, edit or add spoken lines or hooks yourself, and never send a generated script through `megaphone_send_script`. That tool only imports text the customer typed themselves.

Ask for one topic. If the customer has none, suggest at most three topics grounded in confirmed answers. If they want openings first, call `megaphone_suggest_hooks` with the idea (or a video link), show every returned hook unchanged with its pick, and let them choose one; a chosen hook becomes `openingLine` in the script request.

Submit one request with `megaphone_generate_script`: a new stable `requestId`, the exact topic, `voiceId` when several ready voices exist, and `openingLine` when they chose a hook. Teaching is the default; use `intent: invite` with a `keyword` only when the customer asks for that call to action. Keep the `requestId`. Megaphone's worker writes, checks and saves the script to the iPhone library by itself; there is nothing to import.

While the result is queued or running, say once that it's being written, then read progress with the same `requestId` and `operation: status`. Status never starts another paid run. Never submit a second request to work around a slow or uncertain one. If it comes back blocked or needing input, say plainly what the customer must do, using the returned message.

When it is saved, show the title, length and opening line, then offer only the returned next actions in plain words: read the script, make it stronger, see what it's built on, or try a new angle. Never show IDs, versions, state names or tool names.

- **Read:** show the saved lines from `megaphone_coach` with the script ID.
- **Make it stronger:** call `megaphone_upgrade_script` with the exact script ID and version. Show every word of the preview, the biggest leak and the changes, then ask whether to keep the stronger version or stay with the original. Keeping it calls `megaphone_edit_script_copy` with the upgrade event; it saves a separate copy and leaves the original unchanged. Staying calls the upgrade with `operation: decline`.
- **What it's built on:** show the returned source labels in plain words.
- **New angle:** a new `megaphone_generate_script` request with a new `requestId`.

Only say a script is in the library after the tool result says it was saved. For a real acceptance test, also ask the customer to confirm the same script is visible in the iPhone app.
