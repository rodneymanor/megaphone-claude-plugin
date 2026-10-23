# Megaphone for Claude

This repository packages the Megaphone connector and two customer skills: Setup and Script Writer. The plugin uses the hosted connector at `https://joinmegaphone.com/mcp`. It contains no credentials or local programs.

The package under `plugins/megaphone/` matches version 0.2.0 tested in Claude chat and on an iPhone on October 23, 2026. The approved script was imported into the phone library and matched the connector's synced library readback.

In Claude, add `https://github.com/rodneymanor/megaphone-claude-plugin` under **Customize → Plugins → Add plugin → Add marketplace**, install **Megaphone**, and connect your Megaphone account from the plugin's **Connectors** tab. Approval happens on your iPhone. Say “Help me set up Megaphone,” then “Write a Megaphone script about [topic].” A script is sent only after you keep the exact text; open Megaphone to import it.

The `Megaphone-0.2.0.zip` release asset is the fallback upload for Claude's plugin dialog. Validate both the plugin and marketplace before release:

```sh
claude plugin validate ./plugins/megaphone
claude plugin validate .
```

The plugin does not schedule posts or run customer DMs. Other crew roles are outside this first-script release.

The tested account was a paid Claude chat account. A fresh customer account, free-plan support, Cowork, and a full Claude Code sign-in have not yet been verified.
