---
name: weekly-review
description: Walks the trader through their trading week in Journalit (results, best and worst trades, mistakes, setup adherence, goals) and drafts their weekly review for them to approve before anything is saved. Use when the user asks to review their week, do their weekly review or reflect on the last five sessions.
license: MIT
compatibility: Requires the Journalit MCP server with review write access.
metadata:
  author: journalit
  tier: official
  version: "1.0.0"
  journalit-tools: "inspect_journal evaluate_trades analyze_behavior query_trades get_review describe_actions apply_changes navigate_journalit"
  writes: "true"
---

# Weekly review

1. Read the core skill: call `read_skill` with no arguments and follow it, including `references/coaching.md` and `references/trades-reviews-integrations.md`. Its rules win over anything here.
2. Resolve the week: call `inspect_journal` with `session_mode` for the time zone, then confirm with the user which week (default: the most recent completed one).
3. Gather, keeping counted calls few:
   - `evaluate_trades` for the week: net result, win rate, average win and loss, by setup.
   - `analyze_behavior` with `mistake_cost` for the week.
   - `query_trades` for the best and worst two trades (bounded fields, one page).
   - `get_review` for the week, to see what already exists and last week's goals. Ask only for the sections you need.
4. Talk it through with the user before writing anything. Ask two or three questions: what went well, what they would do differently, what to focus on next week. Use their answers, not your guesses.
5. Draft the review text from their answers and the numbers. Show it to them and let them edit it.
6. To save it: call `describe_actions` to see which review actions exist and their inputs, then preview with `apply_changes`. Show the user every action's preview summary, and whether Journalit will ask them to approve it in the app.
7. Ask the user before committing, unless they have told you to commit without asking. Only commit the exact preview they agreed to, with a new idempotency key. If they want changes, build a new preview.
8. Report the outcome. On `approval_pending`, tell them to approve it on the card in Journalit. On `approval_denied`, stop. Offer `navigate_journalit` to open the saved review.

Coaching, not advice: reflect their own data and words back, do not diagnose, do not promise results.
