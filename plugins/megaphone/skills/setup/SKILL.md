---
name: setup
description: Set up or resume a customer's Megaphone content bank by asking only missing questions, saving each confirmed answer, and checking custom voice readiness. Use for Megaphone setup or onboarding.
---

# Megaphone Setup

Use the Megaphone connector bundled with this plugin. The customer's connected account is the only source of identity. Never request a password, token, phone code, UID, or a new account in chat. If a tool is unavailable or reports missing permission, direct the customer to **Customize > Plugins > Megaphone > Connectors** to connect or reconnect Megaphone and approve access on their phone. Do not add a second connector.

Start with `megaphone_account`, `megaphone_content_context`, and `megaphone_list_voices`. An authenticated account check is stronger than a visible connector badge. Treat only the returned confirmed onboarding source as saved bot answers. Do not read or write the iPhone creator brief or infer answers from unrelated scripts, uploads, research, or chat history.

If setup is already complete, report it and do not ask the seven questions again. Check ready synced custom voices separately. With none, direct the customer to finish a custom writing voice in the updated Megaphone iPhone app and sync it. With more than one, let the customer choose during script creation. A preset is not a substitute.

For incomplete setup, explain once: “I'll save your answers as we go, so you can come back later.” Ask only the first missing area, one question at a time, using the returned `missing` list. The compatible areas are:

1. `audience`: Who do you help, and what are they trying to do?
2. `offers`: What do you offer them, if anything?
3. `background`: What experience or perspective should a viewer know about you?
4. `opinions`: What do you believe about this topic that others may disagree with?
5. `stories`: What real example or customer story can you tell?
6. `results`: What result or milestone can you truthfully claim?
7. `customerQuestions`: What do your customers ask most often?

These are missing areas, not demands for seven fresh facts. Accept a direct answer, “none yet,” or “skip” exactly as given; never invent a result, story, offer, or customer question. Silence is not an answer. Ask for confirmation only if you interpret, combine, or rewrite the customer's words. A direct answer needs no second confirmation.

Save each answer immediately with `megaphone_save_answers`: pass one `changes` entry with its `questionId` and exact answer, the `sourceId` most recently returned by `megaphone_content_context` or the previous save as `expectedSourceId` (including `null` initially), today's ISO date, and one unique `saveId` retained for this exact packet. Leave `sectionText` and `sectionUpdates` out unless the customer confirmed a rewrite. The tool merges other answers. Never send a whole replacement brief.

After an uncertain save, read `megaphone_content_context` before acting. If the exact answer appears, continue. If it does not and the source ID is unchanged, retry the identical packet with the original date and `saveId`. If the source changed, reconcile the new context with the customer; never overwrite it silently. After each confirmed save, use the returned source ID for the next answer. If a later chat resumes, read context again instead of relying on chat memory.

Claim “setup saved” only when a fresh `megaphone_content_context` returns `status: complete` and all seven areas answered. Report voice readiness as a separate prerequisite. Offer Megaphone Script when both are ready.
