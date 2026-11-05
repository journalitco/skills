# Contributing a skill

Thanks for sharing your workflow. A good skill is something you already do with your agent and Journalit that other traders would want too.

## 1. Make the folder

```
skills/
  your-skill-name/
    SKILL.md          required
    references/       optional, more Markdown the skill links to
    examples/         optional, sample prompts or outputs (no real journal data)
```

The folder name must match the `name` in the frontmatter: lowercase letters, numbers and single hyphens, up to 64 characters.

Only Markdown (`.md`) and images (`.png`, `.jpg`, `.webp`) are allowed. No scripts.

## 2. Write SKILL.md

```markdown
---
name: your-skill-name
description: What it does and when the agent should use it, in one or two sentences (max 1024 characters).
license: MIT
compatibility: Requires the Journalit MCP server.
metadata:
  author: your-github-or-discord-handle
  tier: community
  version: "1.0.0"
  journalit-tools: "inspect_journal query_trades evaluate_trades"
  writes: "false"
---

# Your skill

1. Read the core skill: call `read_skill` with no arguments and follow it.
2. ...
```

Rules:

- **`journalit-tools`** lists every Journalit tool the skill uses. CI checks these are real tool names.
- **`writes`** is `"true"` if the skill ever calls `apply_changes`. If so, the skill must say, in its own words, to preview, show the user the summary and ask before committing. CI checks for an "ask the user before committing" step.
- Start with step 1 above: the core skill holds the rules that keep the user's journal safe, and it changes as Journalit changes.
- Never tell the agent to skip previews, commit without asking, retry after an approval is denied, or ask the user to give agents full access.
- Never paste real journal data, account numbers or screenshots of someone's P&L into examples.
- No financial advice, profit promises or mental health diagnosis. Coaching is fine; "you have a gambling problem" is not.
- Keep it short. Agents follow a clear 30-line skill better than a 300-line one. Put long material in `references/`.

## 3. Test it

Run the skill with your own agent and your own journal at least once, end to end. In the pull request, say which agent you used and what happened.

Run the validator locally:

```sh
python3 scripts/validate_skills.py
```

## 4. Open a pull request

Fill in the template. A maintainer will review it for safety and clarity, may suggest edits, and merges it once it passes. By contributing you agree your skill is released under its declared licence (MIT by default).

## Updating or removing a skill

Authors can update their own skills by pull request; bump `metadata.version`. Maintainers may edit or remove any skill that breaks the rules or stops working with the current Journalit tools.
