---
name: stock-swing-trader
description: Swing trading system for US stocks using Colin Seow's TraderGPS strategy with MA crossover, volume confirmation, and systematic exits. Use when user says "scan stocks", "check positions", "backtest strategy", "stock alerts", or wants to run daily stock trading analysis. Monitors watchlist for buy/sell signals, tracks open positions, sends Telegram alerts, and provides backtesting capabilities.
---

# Stock Swing Trader

Automated swing trading system based on Colin Seow's TraderGPS strategy with moving average crossovers, volume confirmation, and systematic risk management.

## Quick Start

### First-Time Setup

1. **Configure the skill:**
   ```bash
   python scripts/trader.py --setup
   ```
   This will prompt for:
   - Telegram bot token and chat ID
   - Path to watchlist CSV file
   - Confirm strategy parameters (20/50 MA, 5%/3% exits)

2. **Prepare your watchlist:**
   - Create a CSV file with US stock tickers (see `assets/watchlist-template.csv`)
   - Format: Single column with header "ticker"
   - Select 10 stocks to monitor per month

### Daily Usage

**Scan for signals and monitor positions:**
```bash
python scripts/trader.py
```

This will:
- Check all watchlist stocks for buy signals
- Monitor open positions for exit signals
- Send Telegram alerts for new signals
- Update positions and trade log

**Run backtest:**
```bash
python scripts/trader.py --backtest
```

## Strategy Rules

### Entry Criteria (ALL must be true)

1. **Trend confirmation**: 20-day MA crosses above 50-day MA
2. **Volume spike**: Today's volume ≥ 1.5x the 20-day average volume
3. **Minimum liquidity**: Average volume ≥ 500K shares/day
4. **Market regime**: S&P 500 is above its 50-day MA

### Exit Criteria (ANY triggers exit)

1. **Profit target**: Price reaches +5% from entry
2. **Stop loss**: Price falls to -3% from entry
3. **Trend reversal**: 20-day MA crosses below 50-day MA

### Position Management

- Maximum 10 active positions (one per watchlist stock)
- Entry price: Close price on signal day
- Positions tracked in `data/positions.json`
- All trades logged to `data/trade_log.csv`

## Telegram Alerts

Alerts include:

**Buy Signal:**
```
🟢 BUY: AAPL at $175.50
Stop: $170.23 (-3.0%)
Target: $184.28 (+5.0%)
Volume: 75.2M (1.6x avg)
S&P 500: Bullish ✓
```

**Exit Signal:**
```
🔴 SELL: AAPL at $184.50
Entry: $175.50
P&L: +5.1% (+$9.00)
Reason: Profit target hit
Days held: 8
```

**Position Update (Daily):**
```
📊 Open Positions: 3
AAPL: +3.2% (6 days)
MSFT: -1.5% (3 days)
NVDA: +4.8% (12 days)
```

## Backtesting

Backtest mode simulates the strategy over the past 3 months on current watchlist stocks:

```bash
python scripts/trader.py --backtest
```

**Output metrics:**
- Total trades
- Win rate (% profitable)
- Average gain on winners
- Average loss on losers
- Profit factor (gross profit / gross loss)
- Max drawdown
- Total return

**Example output:**
```
📈 Backtest Results (90 days)
━━━━━━━━━━━━━━━━━━━━━━
Total trades: 24
Wins: 16 (66.7%)
Losses: 8 (33.3%)
Avg win: +4.3%
Avg loss: -2.7%
Profit factor: 2.56
Max drawdown: -8.2%
Total return: +14.8%
```

## Files and Data

**Configuration:**
- `data/config.json` - Telegram credentials, watchlist path, strategy parameters

**Position tracking:**
- `data/positions.json` - Current open positions with entry details
- `data/trade_log.csv` - Complete trade history with entry/exit/P&L

**Logs:**
- `data/scan_log.txt` - Daily scan results and signal details

## Earnings Awareness

The system flags positions approaching earnings (within 7 days) in daily updates:

```
⚠️ AAPL earnings in 3 days - Consider exit before event
```

No automatic action is taken - user decides whether to hold through earnings.

## Strategy Details

See `references/strategy.md` for comprehensive strategy documentation including:
- Detailed entry/exit logic
- Market regime filter rationale
- Volume calculation methodology
- Edge cases and handling

## Telegram Setup

If you need help configuring your Telegram bot, see `references/telegram-setup.md` for step-by-step instructions.

## Dependencies

Required Python packages (auto-installed on first run):
- yfinance (Yahoo Finance data)
- pandas (data manipulation)
- requests (Telegram API)
- python-telegram-bot (Telegram integration)

## Troubleshooting

**"No buy signals found"**
- Market regime may be bearish (S&P 500 below 50-day MA)
- No volume spikes in watchlist stocks
- All stocks already have open positions

**"Telegram alerts not sending"**
- Verify bot token and chat ID in `data/config.json`
- Check bot permissions in Telegram
- See `references/telegram-setup.md`

**"Data fetch errors"**
- Yahoo Finance may be rate-limiting
- Check internet connection
- Verify ticker symbols in watchlist are valid
