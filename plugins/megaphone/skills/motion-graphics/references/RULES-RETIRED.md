# Auto-edit rules: retired here (2026-11-20, PROJ-895)

`BREAKDOWN.md`, `STRAIGHT-TALK.md`, `EDIT-RULES.md` and `edit-rules.json` in this folder are a frozen backup.

The one source of the auto-edit rules is Megaphone's server: Gen-C-A
`apps/next14-standalone/src/server/auto-edit/rules/`. The iPhone app asks the server for an auto edit,
and the server writes the plan from those files. Nothing reads this folder for that.

The backup is also tagged in this repo: `rules-backup-2026-11-20`.
