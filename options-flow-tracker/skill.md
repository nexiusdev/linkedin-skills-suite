---
name: options-flow-tracker
description: Track unusual options flow across S&P 500, Nasdaq, and Dow stocks to identify institutional "whale" trades. Detects golden sweeps, unusual volume spikes, and large block trades with $50K+ premiums. Sends Telegram alerts for significant bullish/bearish flow. Use when the user wants to monitor options market activity, follow smart money, identify potential stock moves based on options positioning, or receive alerts about unusual options trading activity.
---

# Options Flow Tracker

Track institutional options activity across major US indices to identify high-conviction trades.

## Overview

This skill monitors unusual options flow across ~600 stocks (S&P 500 + Nasdaq + Dow) to detect:
- **Golden Sweeps**: Aggressive multi-strike buying ($100K+ premium)
- **Unusual Volume**: Volume 5x+ open interest (new positions)
- **Large Prints**: Single trades $50K+ (institutional size)
- **Flow Direction**: Bullish vs bearish sentiment

## Workflow

### Telegram Bot Control (NEW - Recommended)
```bash
start_telegram_bot.bat
```

Starts a Telegram bot listener that responds to your commands:
- Send `/scan` to trigger a full options flow scan
- Send `/status` to check today's flow statistics
- Send `/help` to see available commands

This runs as a background service - leave it running and control scans from your phone!

**Available Commands:**
- `/scan` or `scan` - Run complete flow scan and analysis
- `/status` - View today's flow stats (signals, tickers, premium)
- `/help` - Show command list

### Daily Automated Scan (Traditional Method)
```bash
run_daily_scan.bat
```

Runs the complete 2-step workflow:
1. **Scanner**: Detects all unusual flow and logs to CSV
2. **Analyzer**: Filters, ranks, and sends consolidated recommendation report

This is the traditional scheduled approach - you'll receive ONE comprehensive report instead of dozens of individual alerts.

### Manual Scanner Only
```bash
python scripts/flow_scanner.py
```

Scans all tracked stocks for unusual options activity and sends individual Telegram alerts for each signal. Use this if you want real-time alerts during the scan.

### Manual Analyzer Only
```bash
python scripts/flow_analyzer.py
```

Analyzes today's logged signals and generates a prioritized recommendation report. Use this to re-analyze signals without re-scanning.

### Setup
```bash
python scripts/flow_scanner.py --setup
```

Configure Telegram credentials (reuses stock-swing-trader config if available).

## Signal Types

### 1. Golden Sweep
- Multi-strike aggressive buying
- Premium $100K+
- High conviction institutional bet
- **Action**: Strong directional signal

### 2. Unusual Volume
- Volume > 5x open interest
- Indicates NEW large positions
- Not just existing positions closing
- **Action**: Monitor for continuation

### 3. Large Block Trade
- Single trade $50K+
- Often institutional or hedge fund
- Check if near bid (selling) or ask (buying)
- **Action**: Note direction and follow

## Flow Interpretation

### Bullish Signals
- Large call buying (at/near ask)
- Large put selling
- Call sweeps above current price
- Call volume >> put volume

### Bearish Signals
- Large put buying (at/near ask)
- Large call selling
- Put sweeps below current price
- Put volume >> call volume

## Alert Screening & Recommendations

The system includes intelligent alert filtering to help you focus on the highest-conviction plays:

### How It Works
1. **Scanner** detects ALL unusual flow (raw signals logged to CSV)
2. **Analyzer** processes signals through multi-factor scoring:
   - Signal quality (Golden Sweep > Unusual Volume > Large Block)
   - Premium size ($1M+ = highest score)
   - Strike distance (closer to current price = higher probability)
   - DTE optimization (14-45 days = sweet spot)
   - Signal clustering (multiple signals on same ticker = higher conviction)
   - Direction consistency (all bullish or bearish = clearer signal)

### Conviction Levels
- **VERY HIGH (70-100)**: Strong institutional flow - consider immediate action
- **HIGH (60-70)**: Solid conviction - monitor for entry
- **MODERATE (50-60)**: Interesting - add to watchlist
- **LOW (<50)**: Informational only

### Report Format
Top 10 highest-conviction plays ranked by score, with:
- Ticker, direction, conviction level
- Total premium and signal count breakdown
- Key strike concentrations
- **Actionable recommendations**: BUY STOCK, BUY CALLS, AVOID LONGS, WATCHLIST, etc.

### Special Cases
- **MIXED signals**: When both bullish and bearish flow detected - action is "WAIT"
- **Clustered strikes**: Multiple signals on same strike = high institutional interest
- **Massive premium**: $10M+ on single ticker = extraordinary conviction

## Individual Alert Format

When running scanner only, individual Telegram alerts include:
- Ticker and signal type
- Strike, expiration, call/put
- Premium and contract count
- Stock price and implied move
- Bullish/bearish interpretation

## Risk Management

### For Beginners
1. **Paper trade first** - Track signals for 1-3 months before real money
2. **Position sizing** - Never risk >2-5% per trade
3. **Use as confirmation** - Combine with technical analysis
4. **Focus on liquid stocks** - Major names with tight spreads
5. **Avoid blindly following** - Whales can be wrong too

### Trading Approaches
- **Conservative**: Trade the underlying stock based on flow
- **Moderate**: Buy calls/puts same direction as flow (defined risk)
- **Advanced**: Match exact strikes/expirations (requires experience)

## Data Source

Uses free/delayed options data via yfinance API:
- 15-20 minute delay (sufficient for EOD analysis)
- Cost: $0
- Good for learning and paper trading
- Can upgrade to real-time data later if needed

## Stock Universe

Tracks ~600 stocks across:
- S&P 500: Large-cap US stocks
- Nasdaq 100: Tech-heavy growth stocks
- Dow 30: Blue-chip industrials

Stock list auto-updates from assets/stock-universe.csv

## Scheduling

Set up automatic daily scans with Windows Task Scheduler:
```powershell
.\setup_scheduler.ps1
```

Runs daily at 4:30 PM ET (after market close, before data is stale).

## Educational Resources

- **references/options-flow-basics.md**: Learn options flow fundamentals
- **references/flow-patterns.md**: Common patterns and interpretation
- **references/risk-management.md**: Position sizing and risk rules

## Files

- **scripts/flow_scanner.py**: Main scanner and alert engine
- **scripts/fetch_stock_universe.py**: Update S&P/Nasdaq/Dow lists
- **scripts/telegram_notifier.py**: Send Telegram alerts
- **data/config.json**: Configuration (Telegram, thresholds)
- **data/flow_history.csv**: Historical flow log
- **assets/stock-universe.csv**: Master stock list

## Configuration

Edit `data/config.json` to adjust:
- `min_premium`: Minimum trade size ($50K default)
- `volume_oi_ratio`: Volume/OI threshold (5.0x default)
- `sweep_threshold`: Golden sweep minimum ($100K default)
- `max_dte`: Maximum days to expiration (45 default)

## Performance Tracking

All detected flows logged to `data/flow_history.csv` for analysis:
- Date, ticker, signal type
- Strike, expiration, call/put
- Premium, volume, OI
- Stock price at signal
- Outcome tracking (add manually or via script)
