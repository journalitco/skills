---
name: mistake-audit
description: Works out what the trader's tagged mistakes cost compared with their clean trades, whether losses cluster after losses or late in the day, and which single habit is worth fixing first. Use when the user asks what their mistakes cost, why they keep losing, whether they overtrade or tilt, or what to work on.
license: MIT
compatibility: Requires the Journalit MCP server.
metadata:
  author: journalit
  tier: official
  version: "1.0.0"
  journalit-tools: "inspect_journal analyze_behavior evaluate_trades query_trades"
  writes: "false"
---

# Mistake audit

1. Read the core skill: call `read_skill` with no arguments and follow it, including `references/performance.md`.
2. Agree the window with the user (default: the last 30 trading days) and the account, if they have more than one. Use `inspect_journal` to resolve account IDs; never guess them.
3. Run `analyze_behavior` three times, one pattern each: `mistake_cost`, then `tilt`, then `overtrading`, for the same window and account.
4. If a mistake stands out, you may make one `evaluate_trades` call to break it down by setup or time of day. Only fetch example trades with `query_trades` (bounded fields, one page) if the user wants to see them.
5. Report:
   - A small table: mistake, number of trades, total cost, cost per trade, compared with clean trades.
   - Whether tilt or overtrading shows up, with the numbers behind it and the sample size. Say plainly when the sample is too small to conclude anything.
   - **Fix first:** the one mistake with the biggest total cost that the user can act on, and one concrete rule they could try.
6. Keep returned numbers separate from your interpretation, and keep the calculation context (window, account, currency, net or gross).

Describe behaviour, not the person. Do not diagnose psychology or mental health, and do not give financial advice.
