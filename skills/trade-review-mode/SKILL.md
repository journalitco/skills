---
name: trade-review-mode
description: Walks the trader through a session's trades one at a time, asking for setup, thesis, intended risk and a 1-5 rating, and saves each answer to that trade after a preview before moving on. Use when the user says "trade review mode", "enter trade review mode" or wants to review a session's trades one by one.
license: MIT
compatibility: Requires the Journalit MCP server with trade write access.
metadata:
  author: trav009
  tier: community
  version: "1.1.0"
  journalit-tools: "inspect_journal inspect_configuration query_trades describe_actions apply_changes navigate_journalit"
  writes: "true"
---

# Trade review mode

An end-of-session routine: walk the session's trades in time order, ask the same four questions per trade, save the answers, then move to the next one. One trade in flight at a time. Never write to a trade the user has not answered for.

1. Read the core skill: call `read_skill` with no arguments and follow it, including `references/trades-reviews-integrations.md`. Its rules win over anything here. If the journal is offline, relay what the error says to open and stop.
2. Resolve the session:
   - `inspect_journal` with `session_mode` for the time zone and trading-day cutoff. Derive the session window from those, not from UTC midnight; a trading day can run past midnight.
   - `query_trades` for that window, regular trades only, sorted by entry time ascending, one page. Order by entry time, never by note names.
   - Show the ordered list once (time, direction, P&L, short trade id) with the count, so the user can correct the scope before you start.
   - `inspect_configuration` with the `option_catalogs` domain for the setup catalog (name to id). Never invent a setup id or name.
3. For each trade, ask all four in one message as a short numbered list, naming the trade by time, direction, P&L and short id:
   1. Setup
   2. Thesis: why they took it
   3. Intended risk, in the journal's display currency
   4. Rating, 1 to 5
   - "Same as previous" is a complete answer: reuse the four values from the trade just saved and name them back.
   - Tidy a fast-typed thesis into one clean sentence that keeps their meaning, and say what you changed.
   - A skipped answer is a skipped field. Write nothing for it and report it as skipped.
   - If the user's description of trades does not match the session's trades (for example "the first was a CF and BOF trade"), settle the mapping before writing anything.
4. Save each trade before moving on. Call `describe_actions` once for `trade.update`, then per trade preview `apply_changes` with only what the user gave: `setup_id`, `thesis`, `risk_amount`. Show the preview summary and ask before committing, unless the user has told you to commit without asking. Commit only that preview, with a new idempotency key.
5. Rating and a second setup: if the current `trade.update` contract has a field for them, include them in the same preview. If it does not, do not edit note files to work around it. Tell the user which values to set in Journalit (offer `navigate_journalit` to open the trade) and list them in the final report.
6. Verify once at the end with one `query_trades` for the session filtered on the setups written; the row count should match the trades reviewed. Each `query_trades` and commit counts against the monthly allowance, so do not re-read every trade.
7. Report one line per trade as you go. At the end, a table (time, direction, P&L, setup, risk, rating, saved or left for the user), plus anything skipped, every thesis you reworded and every "same as previous" reuse.

Adapting it: you can change the four questions (add a mistake tag, a grade, a screenshot). Change the question list and what you save together, and keep the one-trade-at-a-time and preview-before-commit order.
