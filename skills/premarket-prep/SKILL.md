---
name: premarket-prep
description: Gives the trader a short pre-market brief from their Journalit journal (last lessons, goals, recent mistakes, tilt signals, best and worst setups and hours, prop challenge progress) and one focus for the session. Use when the user says "prep me", "pre-market", "before I trade today" or similar.
license: MIT
compatibility: Requires the Journalit MCP server.
metadata:
  author: journalit
  tier: official
  version: "1.0.0"
  journalit-tools: "inspect_journal get_premarket_brief navigate_journalit"
  writes: "false"
---

# Pre-market prep

1. Read the core skill: call `read_skill` with no arguments and follow it. Its rules win over anything here.
2. Call `inspect_journal` with the `session_mode` section to get the user's time zone and today's trading day. Do not assume the date.
3. Call `get_premarket_brief` for today's trading day. It is one counted call; do not add others unless the user asks a follow-up.
4. Reply in this shape, short enough to read in under a minute:
   - **Last time:** the lesson from the most recent review, in their words if possible.
   - **Watch for:** the one or two mistakes that came up most recently, and the tilt signal if it is raised.
   - **Lean on:** the best setup and time of day; mention the worst one to avoid.
   - **Challenge:** where any prop challenge stands against its limits (distance to daily loss limit and drawdown), if there is one.
   - **One focus for today:** a single, concrete behaviour drawn from the above.
5. If the user wants to look at something, offer `navigate_journalit` to open it (for example the Account Dashboard or yesterday's review). Do not open anything unasked.

Keep it factual and from their own data. This is a checklist, not a trade idea: never suggest instruments, entries, direction or size, and never promise an outcome.
