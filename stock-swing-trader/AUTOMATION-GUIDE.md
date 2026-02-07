# Stock Swing Trader - Automation Guide

## Automated Daily Scans with Telegram Alerts

Your stock scanner is configured to send results to Telegram. This guide explains how to set up automated daily scanning.

---

## Quick Setup (Recommended)

**Option 1: Using the Setup Script**

1. Navigate to the `stock-swing-trader` folder
2. Right-click `SETUP-AUTOMATION.bat`
3. Select "Run as Administrator"
4. Press Enter to accept the default time (5:30 AM) or enter your preferred time
5. The task will be created and run daily

**Option 2: Manual PowerShell Setup**

Open PowerShell as Administrator and run:

```powershell
cd "C:\Users\melve\.claude\skills\stock-swing-trader"
.\scripts\setup-automation.ps1
```

---

## What Gets Automated

The scheduled task will:
- Run every day at 5:30 AM (after US market close, data settled)
- Scan all 120 stocks in your watchlist
- Check for buy signals (MA crossover + volume spike)
- Monitor any open positions for exit signals
- Send a summary to your Telegram

---

## Telegram Notifications

You'll receive messages like:

**When signals are found:**
```
🟢 BUY: AAPL at $150.50
Stop: $145.99 (-3.0%)
Target: $158.03 (+5.0%)
Volume: 75.2M (1.6x avg)
S&P 500: Bullish ✓
```

**Daily summary (no signals):**
```
📊 Stock Scan Complete
Date: 2026-01-30
Market: Bullish ✓
Signals: 0 new
Positions: 0 open
```

**When exits are triggered:**
```
🔴 SELL: AAPL at $158.25
Entry: $150.50
P&L: +5.1% (+$7.75)
Reason: Profit target hit
Days held: 8
```

---

## Managing the Scheduled Task

### View Task Status
```powershell
Get-ScheduledTask -TaskName "StockSwingTrader-DailyScan"
```

### Run Scan Immediately
```powershell
Start-ScheduledTask -TaskName "StockSwingTrader-DailyScan"
```

### Disable Automatic Scanning
```powershell
Disable-ScheduledTask -TaskName "StockSwingTrader-DailyScan"
```

### Re-enable Automatic Scanning
```powershell
Enable-ScheduledTask -TaskName "StockSwingTrader-DailyScan"
```

### Remove the Task Completely
```powershell
Unregister-ScheduledTask -TaskName "StockSwingTrader-DailyScan" -Confirm:$false
```

### Change the Scan Time
```powershell
# Remove existing task
Unregister-ScheduledTask -TaskName "StockSwingTrader-DailyScan" -Confirm:$false

# Run setup again with new time
cd "C:\Users\melve\.claude\skills\stock-swing-trader"
.\scripts\setup-automation.ps1
```

---

## Manual Scanning

You can always run a scan manually instead of waiting for the scheduled time:

```bash
cd stock-swing-trader
python scripts/trader.py
```

This will scan all stocks and send results to Telegram immediately.

---

## Scan Timing Recommendation

**Default: 5:30 AM SGT (Singapore Time)**

This timing works well because:
- US market closes at 4:00 PM ET
- That's 5:00 AM SGT (winter) or 4:00 AM SGT (summer)
- 5:30 AM gives 30-90 minutes for data to settle
- Alerts arrive before your morning routine

**Alternative times:**
- **6:00 AM** - If you wake up early and want alerts with breakfast
- **7:00 AM** - More conservative, ensures all data is final
- **9:00 PM ET / 10:00 AM SGT** - For traders who prefer to review mid-morning

---

## Troubleshooting

**Task won't create - "Access Denied"**
- Make sure you run the setup script as Administrator
- Right-click → "Run as Administrator"

**No Telegram messages**
- Check your bot token and chat ID in `data/config.json`
- Test manually: `python scripts/telegram_notifier.py --test`
- Check the automation log: `data/automation.log`

**Scan not running at scheduled time**
- Verify the task is enabled: `Get-ScheduledTask -TaskName "StockSwingTrader-DailyScan"`
- Check if your computer is on at the scheduled time (task won't run if PC is off)
- Enable "Start the task as soon as possible after a scheduled start is missed" in Task Scheduler

**Computer is off at scan time**
The task won't run if your PC is asleep or shutdown. Options:
1. Change the scan time to when your PC is usually on
2. Leave your PC on or use "sleep" mode (task can wake from sleep if configured)
3. Run scans manually when convenient

---

## Files Created

- `scripts/run-daily-scan.bat` - The script that runs each day
- `scripts/setup-automation.ps1` - PowerShell setup wizard
- `data/automation.log` - Log of scan executions
- Windows Task Scheduler entry: "StockSwingTrader-DailyScan"

---

## Testing Your Setup

After setup, test that everything works:

1. **Test Telegram connection:**
   ```bash
   cd stock-swing-trader
   python scripts/telegram_notifier.py --test
   ```

2. **Test the scan manually:**
   ```bash
   python scripts/trader.py
   ```

3. **Test the scheduled task:**
   ```powershell
   Start-ScheduledTask -TaskName "StockSwingTrader-DailyScan"
   ```
   Check your Telegram - you should receive the scan results within 1-2 minutes.

---

## Next Steps

Once automation is set up:

1. **Check Telegram each morning** for overnight signals
2. **Review any buy signals** before market open (9:30 AM ET / 10:30 PM SGT)
3. **Execute trades** during market hours if you approve the signal
4. **Log your trades** - the system tracks positions automatically after you enter them

The scanner is conservative and selective - expect 1-2 signals per month across your 120-stock watchlist. Quality over quantity.
