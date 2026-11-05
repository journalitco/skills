---
name: trade-review-mode
description: Reviews the trader's trades one at a time in a guided session (plan, execution, emotions, mistakes, lesson) and, if they want, saves notes and mistake tags to each trade after they approve the preview. Use when the user wants to go through their trades one by one or enter trade review mode.
license: MIT
compatibility: Requires the Journalit MCP server with trade write access.
metadata:
  author: trav009
  tier: community
  version: "0.1.0"
  journalit-tools: "inspect_journal query_trades get_trade view_image describe_actions apply_changes navigate_journalit"
  writes: "true"
---

# Trade review mode

> Placeholder. To be replaced with @trav009's original "Trade Review Mode" skill from Discord, with his permission and credit, then adapted to the rules below.

1. Read the core skill: call `read_skill` with no arguments and follow it.
2. Ask which trades to review (default: today's trading day). Use `query_trades` with bounded fields and one page to list them.
3. For each trade, one at a time:
   - `get_trade` with only the sections needed (summary, notes with `notes_max_chars`, media). Use `view_image` only for the chart the user wants to discuss.
   - Offer `navigate_journalit` to open the trade so they can look at it too.
   - Ask: what was the plan, did you follow it, what did you feel, was there a mistake, what is the lesson. Wait for their answers.
4. Collect the notes and mistake tags for all reviewed trades. Then call `describe_actions`, and preview one `apply_changes` batch.
5. Show the preview summary for every trade and ask the user before committing. Commit only that preview.
6. Report each outcome. Stop on `approval_denied`.
