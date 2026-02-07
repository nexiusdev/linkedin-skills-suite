#!/usr/bin/env python3
"""
Stock Swing Trader - Colin Seow's TraderGPS Strategy
Main script for scanning stocks and monitoring positions
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Auto-install dependencies on first run
try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance", "pandas", "requests", "python-telegram-bot"])
    import yfinance as yf
    import pandas as pd

from data_fetcher import fetch_stock_data, fetch_spy_data, get_earnings_date
from telegram_notifier import TelegramNotifier


class TraderGPS:
    def __init__(self, config_path: str = "data/config.json", aggressive: bool = False):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.positions_path = Path("data/positions.json")
        self.trade_log_path = Path("data/trade_log.csv")
        self.aggressive = aggressive
        self.notifier = TelegramNotifier(
            self.config.get("telegram_bot_token"),
            self.config.get("telegram_chat_id")
        )

    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        if not self.config_path.exists():
            return {}
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save_config(self):
        """Save configuration to JSON file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def load_positions(self) -> Dict:
        """Load open positions from JSON file"""
        if not self.positions_path.exists():
            return {}
        with open(self.positions_path, 'r') as f:
            return json.load(f)

    def save_positions(self, positions: Dict):
        """Save positions to JSON file"""
        self.positions_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.positions_path, 'w') as f:
            json.dump(positions, f, indent=2)

    def log_trade(self, ticker: str, action: str, price: float,
                  reason: str = "", entry_price: float = None, days_held: int = 0):
        """Log trade to CSV file"""
        self.trade_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create CSV if doesn't exist
        if not self.trade_log_path.exists():
            with open(self.trade_log_path, 'w') as f:
                f.write("date,ticker,action,price,entry_price,pnl_pct,pnl_dollars,days_held,reason\n")

        pnl_pct = pnl_dollars = 0
        if action == "SELL" and entry_price:
            pnl_pct = ((price - entry_price) / entry_price) * 100
            pnl_dollars = price - entry_price

        with open(self.trade_log_path, 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d')},{ticker},{action},{price:.2f},"
                   f"{entry_price or 0:.2f},{pnl_pct:.2f},{pnl_dollars:.2f},{days_held},{reason}\n")

    def check_market_regime(self) -> bool:
        """Check if S&P 500 is above 50-day MA (bullish regime)"""
        try:
            spy_data = fetch_spy_data()
            if spy_data is None or len(spy_data) < 50:
                print("WARNING: Unable to fetch SPY data, defaulting to allowing trades")
                return True

            spy_data['MA50'] = spy_data['Close'].rolling(window=50).mean()
            current_close = spy_data['Close'].iloc[-1]
            ma50 = spy_data['MA50'].iloc[-1]

            is_bullish = current_close > ma50
            status = "Bullish OK" if is_bullish else "Bearish X"
            print(f"Market Regime: {status} (SPY: ${current_close:.2f}, MA50: ${ma50:.2f})")
            return is_bullish
        except Exception as e:
            print(f"WARNING: Error checking market regime: {e}")
            return True  # Fail-safe: allow trades if check fails

    def check_buy_signal(self, ticker: str, data: pd.DataFrame) -> Optional[Dict]:
        """Check if stock has a buy signal"""
        if len(data) < 200:  # Need 200 days for MA200
            return None

        # Calculate moving averages
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['MA50'] = data['Close'].rolling(window=50).mean()
        data['MA200'] = data['Close'].rolling(window=200).mean()
        data['Volume_MA20'] = data['Volume'].rolling(window=20).mean()

        # Get today and yesterday data
        today = data.iloc[-1]
        yesterday = data.iloc[-2] if len(data) > 1 else None

        if yesterday is None:
            return None

        # Filter 1: Minimum Price - Avoid small caps under $10
        if today['Close'] < 10.0:
            return None

        # Filter 2: Volatility - Avoid highly volatile stocks (skip in aggressive mode)
        if not self.aggressive:
            daily_returns = data['Close'].pct_change().tail(20)
            avg_daily_move = daily_returns.abs().mean()
            if avg_daily_move > 0.05:  # Max 5% average daily move
                return None

        # Filter 3: Relative Strength - Price must be above 200-day MA
        if today['Close'] <= today['MA200']:
            return None

        # Filter 4: Trend Confirmation - 50-day MA must be above 200-day MA
        if today['MA50'] <= today['MA200']:
            return None

        # Check crossover: MA20 crosses above MA50
        crossover = (today['MA20'] > today['MA50'] and
                    yesterday['MA20'] <= yesterday['MA50'])

        if not crossover:
            return None

        # Check volume spike: >1.5x average
        volume_spike = today['Volume'] >= (today['Volume_MA20'] * 1.5)

        # Check minimum liquidity: avg volume >= 500K
        avg_volume = today['Volume_MA20']
        sufficient_liquidity = avg_volume >= 500_000

        if not volume_spike or not sufficient_liquidity:
            return None

        # All criteria met - return buy signal
        return {
            'ticker': ticker,
            'entry_price': today['Close'],
            'entry_date': today.name.strftime('%Y-%m-%d'),
            'stop_loss': today['Close'] * 0.97,  # -3%
            'profit_target': today['Close'] * 1.05,  # +5%
            'volume': today['Volume'],
            'avg_volume': avg_volume,
            'volume_ratio': today['Volume'] / avg_volume,
            'ma20': today['MA20'],
            'ma50': today['MA50'],
            'ma200': today['MA200']
        }

    def check_exit_signal(self, ticker: str, position: Dict,
                         data: pd.DataFrame) -> Optional[tuple]:
        """Check if position has an exit signal. Returns (reason, price) or None"""
        if len(data) < 50:
            return None

        # Calculate moving averages
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['MA50'] = data['Close'].rolling(window=50).mean()

        today = data.iloc[-1]
        yesterday = data.iloc[-2] if len(data) > 1 else None
        current_price = today['Close']

        # Check profit target
        if current_price >= position['profit_target']:
            return ("Profit target hit", current_price)

        # Check stop loss
        if current_price <= position['stop_loss']:
            return ("Stop loss hit", current_price)

        # Check MA reversal (20 crosses below 50)
        if yesterday is not None:
            reversal = (today['MA20'] < today['MA50'] and
                       yesterday['MA20'] >= yesterday['MA50'])
            if reversal:
                return ("MA reversal", current_price)

        return None

    def scan_watchlist(self, watchlist: List[str]) -> List[Dict]:
        """Scan watchlist for buy signals"""
        print(f"\n[SCAN] Scanning {len(watchlist)} stocks for signals...\n")

        # Check market regime first
        if not self.check_market_regime():
            print("\n🛑 Market regime is bearish - no new positions")
            return []

        signals = []
        positions = self.load_positions()

        for ticker in watchlist:
            # Skip if already have position
            if ticker in positions:
                continue

            print(f"Checking {ticker}...", end=" ")
            data = fetch_stock_data(ticker)

            if data is None or len(data) < 50:
                print("ERROR: Insufficient data")
                continue

            signal = self.check_buy_signal(ticker, data)
            if signal:
                signals.append(signal)
                print(f"OK BUY SIGNAL")
            else:
                print("No signal")

        return signals

    def monitor_positions(self) -> tuple:
        """Monitor open positions for exit signals"""
        positions = self.load_positions()

        if not positions:
            print("\nNo open positions to monitor")
            return ([], {})

        print(f"\n[SCAN] Monitoring {len(positions)} open positions...\n")

        exits = []
        updated_positions = {}

        for ticker, position in positions.items():
            print(f"Checking {ticker}...", end=" ")
            data = fetch_stock_data(ticker)

            if data is None or len(data) < 50:
                print("ERROR: Cannot fetch data")
                updated_positions[ticker] = position  # Keep position
                continue

            exit_signal = self.check_exit_signal(ticker, position, data)

            if exit_signal:
                reason, exit_price = exit_signal
                entry_date = datetime.strptime(position['entry_date'], '%Y-%m-%d')
                days_held = (datetime.now() - entry_date).days

                exits.append({
                    'ticker': ticker,
                    'exit_price': exit_price,
                    'entry_price': position['entry_price'],
                    'reason': reason,
                    'days_held': days_held
                })

                # Log trade
                self.log_trade(
                    ticker=ticker,
                    action="SELL",
                    price=exit_price,
                    reason=reason,
                    entry_price=position['entry_price'],
                    days_held=days_held
                )

                print(f"OK EXIT: {reason}")
            else:
                # Check earnings warning
                current_price = data['Close'].iloc[-1]
                pnl_pct = ((current_price - position['entry_price']) / position['entry_price']) * 100

                earnings_date = get_earnings_date(ticker)
                if earnings_date and (earnings_date - datetime.now()).days <= 7:
                    days_to_earnings = (earnings_date - datetime.now()).days
                    print(f"WARNING: Earnings in {days_to_earnings} days (P&L: {pnl_pct:+.1f}%)")
                else:
                    print(f"Holding (P&L: {pnl_pct:+.1f}%)")

                updated_positions[ticker] = position

        # Save updated positions
        self.save_positions(updated_positions)

        return (exits, updated_positions)

    def send_alerts(self, signals: List[Dict], exits: List[Dict], positions: Dict):
        """Send Telegram alerts for signals and exits"""
        # Buy signals
        for signal in signals:
            message = (
                f"[BUY] BUY: {signal['ticker']} at ${signal['entry_price']:.2f}\n"
                f"Stop: ${signal['stop_loss']:.2f} (-3.0%)\n"
                f"Target: ${signal['profit_target']:.2f} (+5.0%)\n"
                f"Volume: {signal['volume']/1e6:.1f}M ({signal['volume_ratio']:.1f}x avg)\n"
                f"S&P 500: Bullish OK"
            )
            self.notifier.send_message(message)

        # Exit signals
        for exit in exits:
            pnl_pct = ((exit['exit_price'] - exit['entry_price']) / exit['entry_price']) * 100
            pnl_dollars = exit['exit_price'] - exit['entry_price']
            emoji = "[BUY]" if pnl_pct > 0 else "[SELL]"

            message = (
                f"{emoji} SELL: {exit['ticker']} at ${exit['exit_price']:.2f}\n"
                f"Entry: ${exit['entry_price']:.2f}\n"
                f"P&L: {pnl_pct:+.1f}% ({pnl_dollars:+.2f})\n"
                f"Reason: {exit['reason']}\n"
                f"Days held: {exit['days_held']}"
            )
            self.notifier.send_message(message)

        # Position update summary
        if positions:
            message = f"[SCAN] Open Positions: {len(positions)}\n"

            for ticker, pos in list(positions.items())[:5]:  # Show first 5
                # Fetch current price
                data = fetch_stock_data(ticker)
                if data is not None and len(data) > 0:
                    current_price = data['Close'].iloc[-1]
                    pnl_pct = ((current_price - pos['entry_price']) / pos['entry_price']) * 100
                    entry_date = datetime.strptime(pos['entry_date'], '%Y-%m-%d')
                    days_held = (datetime.now() - entry_date).days
                    message += f"{ticker}: {pnl_pct:+.1f}% ({days_held} days)\n"

            if len(positions) > 5:
                message += f"... and {len(positions) - 5} more"

            self.notifier.send_message(message)

    def run_daily_scan(self):
        """Run daily scan and monitoring workflow"""
        print("=" * 50)
        print("STOCK SWING TRADER - Daily Scan")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

        # Load watchlist
        watchlist_path = self.config.get('watchlist_path')
        if not watchlist_path or not Path(watchlist_path).exists():
            print("\nERROR: Watchlist not found. Run --setup first.")
            return

        with open(watchlist_path, 'r') as f:
            # Skip header, get tickers
            watchlist = [line.strip() for line in f.readlines()[1:] if line.strip()]

        # Scan for buy signals
        signals = self.scan_watchlist(watchlist)

        # Monitor open positions
        exits, positions = self.monitor_positions()

        # Send alerts
        self.send_alerts(signals, exits, positions)

        # Add new positions
        if signals:
            current_positions = self.load_positions()
            for signal in signals:
                ticker = signal['ticker']
                current_positions[ticker] = signal
                self.log_trade(
                    ticker=ticker,
                    action="BUY",
                    price=signal['entry_price'],
                    reason="MA crossover + volume spike"
                )
            self.save_positions(current_positions)

        # Summary
        print("\n" + "=" * 50)
        print(f"OK Scan complete: {len(signals)} new signals, {len(exits)} exits")
        print(f"OK Open positions: {len(positions)}")
        print("=" * 50)

    def setup_wizard(self):
        """Interactive setup wizard"""
        print("=" * 50)
        print("STOCK SWING TRADER - Setup Wizard")
        print("=" * 50)

        # Telegram configuration
        print("\n[Telegram Configuration]")
        print("See references/telegram-setup.md for detailed instructions\n")

        bot_token = input("Enter Telegram bot token: ").strip()
        chat_id = input("Enter Telegram chat ID: ").strip()

        self.config['telegram_bot_token'] = bot_token
        self.config['telegram_chat_id'] = chat_id

        # Watchlist configuration
        print("\n[Watchlist Configuration]")
        watchlist_path = input("Enter path to watchlist CSV file: ").strip()

        if not Path(watchlist_path).exists():
            print(f"ERROR: File not found: {watchlist_path}")
            print("See assets/watchlist-template.csv for format")
            return

        self.config['watchlist_path'] = watchlist_path

        # Strategy parameters (defaults)
        self.config['strategy'] = {
            'ma_fast': 20,
            'ma_slow': 50,
            'profit_target_pct': 5.0,
            'stop_loss_pct': 3.0,
            'volume_multiplier': 1.5,
            'min_avg_volume': 500000
        }

        self.save_config()

        print("\nOK Configuration saved to", self.config_path)
        print("\nTesting Telegram connection...")

        notifier = TelegramNotifier(bot_token, chat_id)
        if notifier.send_message("Stock Trader Alert System Active"):
            print("OK Telegram test successful!")
        else:
            print("ERROR: Telegram test failed. Check your credentials.")

        print("\n" + "=" * 50)
        print("Setup complete! Run 'python scripts/trader.py' to start scanning.")
        print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Stock Swing Trader - TraderGPS Strategy")
    parser.add_argument('--setup', action='store_true', help='Run setup wizard')
    parser.add_argument('--backtest', action='store_true', help='Run backtest mode')
    parser.add_argument('--aggressive', action='store_true',
                       help='Aggressive mode: more signals, lower win rate (disables volatility filter)')

    args = parser.parse_args()

    trader = TraderGPS(aggressive=args.aggressive)

    if args.setup:
        trader.setup_wizard()
    elif args.backtest:
        from backtest import Backtester
        backtester = Backtester(trader.config, aggressive=args.aggressive)
        backtester.run_backtest()
    else:
        trader.run_daily_scan()


if __name__ == "__main__":
    main()
