---
name: script
description: Generate, review, and keep one Megaphone script in the customer's custom voice, then verify its exact iPhone library record. Use for a Megaphone script or when the customer asks to write a script with Megaphone.
---

# Megaphone Script

Use the Megaphone connector bundled with this plugin. First call `megaphone_account`, `megaphone_content_context`, and `megaphone_list_voices`, even when the customer invokes this skill directly. If the connector or a required tool lacks permission, direct them to **Customize > Plugins > Megaphone > Connectors** to reconnect and approve access on their phone. Never ask for credentials or add a second connector.

If onboarding is incomplete, run the Megaphone Setup flow for only the missing areas and resume here after a fresh `megaphone_content_context` says `complete`. Require a ready synced *custom* voice. With none, ask the customer to finish one in the updated Megaphone iPhone app and sync it. With several, ask which voice to use; remember that choice only for this conversation. The generation tool rechecks the account's voice and confirmed bank context. Do not substitute a preset or the experimental iPhone creator brief.

Ask for one topic. If the customer has none, suggest at most three topics grounded in confirmed answers. Ask about unsupported facts before stating them as proof; “none yet” and “skip” are not evidence of a result. Generate one script through `megaphone_generate_script`, with a new stable `requestId`, the selected topic, and `voiceId` when several ready voices exist. Keep that request ID for this generation attempt. Do not automatically retry an uncertain generation or start another paid generation to work around it. Explain `uncertain` or `failed` plainly. A `needs_review` draft may be shown with its issues; do not present it as checked-ready.

Show the generated lines to the customer and flag any assumed lines or unsupported claims. Offer **keep, edit, or skip**. If edited, preserve the exact final lines the customer approved. Do not send until the customer explicitly keeps the specific final text. Skipping ends the flow without delivery. Generation alone does not save a script to the library.

For a kept script, create one stable delivery `requestId` tied to the exact approved lines and call `megaphone_send_script` once with those lines. Reuse the same ID and identical lines if the send result is uncertain; a revision needs a new ID and a new keep decision. Save the returned `expectedLibraryScriptId` and delivery request ID in the conversation. If the result is `queued`, say: “Open Megaphone to import your script.” Queued means the phone has not acknowledged it; do not call it saved, repeatedly poll, or silently resend after expiry.

When the customer returns after opening Megaphone, call `megaphone_delivery_status` with that request ID. If it is `received`, call `megaphone_list_scripts` with the exact `expectedLibraryScriptId`. Verify the returned ID **and** lines match the approved text. A phone acknowledgment can precede cloud sync; if the exact record is missing, say so and check again later without resending. If the delivery expired or was claimed by another account, explain the state and ask before any recovery. Only say “saved in your Megaphone library” after exact synced readback. For a real acceptance test, also ask the customer to confirm that this same script is visible in the iPhone app.
