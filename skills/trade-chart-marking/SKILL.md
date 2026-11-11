---
name: trade-chart-marking
description: Marks a day's journaled trades on a TradingView chart, one risk-reward box per trade, captures a cropped chart image for each and checks it lands on the trade in Journalit. Use when the user wants chart images of their trades drawn on TradingView, or says "mark my trades on the chart".
license: MIT
compatibility: Requires the Journalit MCP server and a TradingView MCP server connected to TradingView Desktop. Saving images needs an agent that can write files in the user's vault.
metadata:
  author: trav009
  tier: community
  version: "1.0.0"
  journalit-tools: "inspect_journal query_trades get_trade view_image"
  writes: "false"
---

# Trade chart marking

Draw each journaled trade on the TradingView chart as a risk-reward box, capture it, file the image with the trade, and prove it arrived. Journalit supplies the trades and confirms the images. TradingView does the drawing.

1. Read the core skill: call `read_skill` with no arguments and follow it, including `references/trades-reviews-integrations.md`. Its rules win over anything here. If the journal is offline, relay what the error says to open and stop.

## Before the first run

Prove each piece once, on one trade, before running a whole day. Stop at the first one that fails and tell the user which.

- **Both servers answer.** The TradingView server's health check returns the chart's symbol and interval, and `inspect_journal` reports the journal online.
- **A box round-trips.** Draw one long or short position box, set its stop and target, and read the prices back off the drawing. If they don't match what you set, nothing after this will be right.
- **Replay works**, if the user wants the chart as it looked at the time. Some TradingView builds expose replay only through the toolbar's own date dialog.
- **An image round-trips.** Capture, crop to the chart, save it into the trade's media folder, then `get_trade` with the `media` section returns a new `media_id`. A file on disk is not proof.

## The run

2. Resolve the day: `inspect_journal` with `session_mode` for the time zone and trading-day cutoff, then `query_trades` for that window, regular trades only, sorted by entry time. Show the list (time, direction, entry, stop, exit, short trade id) and let the user correct it.
3. Ask once whether to draw the day's key levels or whether they are already on the chart. If they are already there, leave them alone.
4. For each trade, in time order:
   - Check the entry and exit prices sit inside their bars and the stop sits beyond the entry bar's extreme. If not, list the trade with both numbers and ask before drawing it.
   - Draw the box from entry to stop to final exit. Ignore partial exits unless the user wants them.
   - Hide every other box, frame at least an hour of one-minute bars around the trade, capture and crop to the chart.
   - Only if the user has agreed to file images in their vault: save the image in that trade's media folder. Otherwise give the user the file and the trade id to attach it themselves.
   - Confirm with `get_trade` (`media` section) that a new `media_id` appeared, and `view_image` it if the user wants to check the picture.
5. Finish: show all boxes again, leave only the last day's levels visible, save the layout and reload the drawings to confirm the count survived.

## Rules

- Never edit the trade note itself. Images go only in the trade's media folder, and only with the user's agreement.
- Drawings belong to the interval that created them. Switch intervals only when you mean to, and re-check the chart cursor afterwards.
- Do not restart TradingView with unsaved drawings.
- Report what you proved, not what you called: how many trades now show an image (with their `media_id`s), how many boxes and levels survived the reload, and every misaligned trade.

## What you supply

Your instrument and tick size, your level definitions if you want levels, your vault's media layout, and how many images you want per trade.
