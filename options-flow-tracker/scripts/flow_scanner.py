#!/usr/bin/env python3
"""
Options Flow Tracker - Smart Money Scanner
Main script for detecting unusual options activity
"""

import sys
import json
import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import time

# Auto-install dependencies on first run
try:
    import yfinance as yf
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance", "pandas", "requests"])
    import yfinance as yf

from telegram_notifier import TelegramNotifier


class OptionsFlowScanner:
    def __init__(self, config_path: str = "data/config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.flow_log_path = Path("data/flow_history.csv")
        self.stock_universe_path = Path("assets/stock-universe.csv")

        # Load configuration
        self.min_premium = self.config.get('min_premium', 50000)  # $50K
        self.sweep_threshold = self.config.get('sweep_threshold', 100000)  # $100K
        self.volume_oi_ratio = self.config.get('volume_oi_ratio', 5.0)  # 5x
        self.min_dte = self.config.get('min_dte', 7)  # 7 days minimum
        self.max_dte = self.config.get('max_dte', 45)  # 45 days maximum

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

    def load_stock_universe(self) -> List[str]:
        """Load stock list with priority for user's watchlist"""
        priority_tickers = []
        remaining_tickers = []

        # Load user's priority stocks from stock-swing-trader watchlist
        user_watchlist_path = Path("../stock-swing-trader/data/watchlist_all.csv")
        if user_watchlist_path.exists():
            try:
                with open(user_watchlist_path, 'r') as f:
                    # Skip header, get tickers
                    priority_tickers = [line.strip() for line in f.readlines()[1:] if line.strip()]
                print(f"Loaded {len(priority_tickers)} priority stocks from swing trader watchlist")
            except Exception as e:
                print(f"Warning: Could not load priority watchlist: {e}")

        # Load full stock universe
        if not self.stock_universe_path.exists():
            print(f"ERROR: Stock universe file not found: {self.stock_universe_path}")
            return priority_tickers

        df = pd.read_csv(self.stock_universe_path)
        all_tickers = df['ticker'].unique().tolist()

        # Remove priority tickers from full list to avoid duplicates
        priority_set = set(priority_tickers)
        remaining_tickers = [t for t in all_tickers if t not in priority_set]

        # Return priority stocks first, then remaining
        final_list = priority_tickers + remaining_tickers
        print(f"Total stocks to scan: {len(final_list)} ({len(priority_tickers)} priority + {len(remaining_tickers)} remaining)")

        return final_list

    def fetch_options_chain(self, ticker: str) -> Optional[Dict]:
        """Fetch options chain for a ticker"""
        try:
            stock = yf.Ticker(ticker)
            expirations = stock.options

            if not expirations:
                return None

            # Get current stock price
            stock_info = stock.info
            current_price = stock_info.get('currentPrice') or stock_info.get('regularMarketPrice')

            if not current_price:
                return None

            return {
                'ticker': ticker,
                'current_price': current_price,
                'expirations': expirations,
                'stock_obj': stock
            }
        except Exception as e:
            print(f"  ERROR fetching {ticker}: {e}")
            return None

    def analyze_options_flow(self, chain_data: Dict) -> List[Dict]:
        """Analyze options chain for unusual activity"""
        ticker = chain_data['ticker']
        current_price = chain_data['current_price']
        stock = chain_data['stock_obj']
        signals = []

        try:
            for expiration in chain_data['expirations']:
                # Calculate days to expiration
                exp_date = datetime.strptime(expiration, '%Y-%m-%d')
                dte = (exp_date - datetime.now()).days

                # Skip if outside DTE range (7-45 days for swing trades)
                if dte > self.max_dte or dte < self.min_dte:
                    continue

                # Get calls and puts
                try:
                    calls = stock.option_chain(expiration).calls
                    puts = stock.option_chain(expiration).puts
                except Exception:
                    continue

                # Analyze calls
                for _, row in calls.iterrows():
                    signal = self.check_unusual_activity(
                        ticker, row, 'CALL', current_price, dte
                    )
                    if signal:
                        signals.append(signal)

                # Analyze puts
                for _, row in puts.iterrows():
                    signal = self.check_unusual_activity(
                        ticker, row, 'PUT', current_price, dte
                    )
                    if signal:
                        signals.append(signal)

        except Exception as e:
            print(f"  ERROR analyzing {ticker}: {e}")

        return signals

    def check_unusual_activity(self, ticker: str, option_row: pd.Series,
                               option_type: str, stock_price: float,
                               dte: int) -> Optional[Dict]:
        """Check if option shows unusual activity"""
        try:
            volume = option_row.get('volume', 0) or 0
            open_interest = option_row.get('openInterest', 0) or 0
            last_price = option_row.get('lastPrice', 0) or 0
            strike = option_row.get('strike', 0)
            bid = option_row.get('bid', 0) or 0
            ask = option_row.get('ask', 0) or 0

            # Skip if no volume
            if volume <= 0 or last_price <= 0:
                return None

            # Calculate premium
            premium = volume * last_price * 100  # Options are 100 shares

            # Check minimum premium threshold
            if premium < self.min_premium:
                return None

            # Determine signal type and direction
            signal_type = None
            direction = None

            # 1. Check for Golden Sweep (high premium + unusual activity)
            if premium >= self.sweep_threshold:
                if open_interest > 0 and volume >= open_interest * 2:
                    signal_type = "Golden Sweep"
                    # Determine if aggressive buying or selling
                    if ask > 0 and last_price >= (bid + ask) / 2:
                        direction = "BULLISH" if option_type == "CALL" else "BEARISH"
                    else:
                        direction = "BEARISH" if option_type == "CALL" else "BULLISH"

            # 2. Check for Unusual Volume (volume >> open interest)
            elif open_interest > 0 and volume >= open_interest * self.volume_oi_ratio:
                signal_type = "Unusual Volume"
                direction = "BULLISH" if option_type == "CALL" else "BEARISH"

            # 3. Check for Large Block Trade
            elif premium >= self.min_premium * 2:  # 2x minimum for block trades
                signal_type = "Large Block"
                if ask > 0 and last_price >= (bid + ask) / 2:
                    direction = "BULLISH" if option_type == "CALL" else "BEARISH"
                else:
                    direction = "BEARISH" if option_type == "CALL" else "BULLISH"

            if not signal_type:
                return None

            # Calculate implied move
            strike_distance = abs(strike - stock_price) / stock_price * 100

            return {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ticker': ticker,
                'signal_type': signal_type,
                'direction': direction,
                'option_type': option_type,
                'strike': strike,
                'expiration': dte,
                'volume': int(volume),
                'open_interest': int(open_interest),
                'premium': premium,
                'stock_price': stock_price,
                'strike_distance': strike_distance,
                'last_price': last_price
            }

        except Exception as e:
            print(f"    ERROR checking option: {e}")
            return None

    def log_flow(self, signal: Dict):
        """Log detected flow to CSV"""
        self.flow_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create CSV if doesn't exist
        if not self.flow_log_path.exists():
            with open(self.flow_log_path, 'w') as f:
                f.write("timestamp,ticker,signal_type,direction,option_type,strike,expiration_dte,"
                       "volume,open_interest,premium,stock_price,strike_distance,last_price\n")

        with open(self.flow_log_path, 'a') as f:
            f.write(f"{signal['timestamp']},{signal['ticker']},{signal['signal_type']},"
                   f"{signal['direction']},{signal['option_type']},{signal['strike']},"
                   f"{signal['expiration']},{signal['volume']},{signal['open_interest']},"
                   f"{signal['premium']:.2f},{signal['stock_price']:.2f},"
                   f"{signal['strike_distance']:.2f},{signal['last_price']:.2f}\n")

    def send_alert(self, signal: Dict):
        """Send Telegram alert for detected flow"""
        ticker = signal['ticker']
        signal_type = signal['signal_type']
        direction = signal['direction']
        option_type = signal['option_type']
        strike = signal['strike']
        dte = signal['expiration']
        premium = signal['premium']
        volume = signal['volume']
        stock_price = signal['stock_price']
        strike_distance = signal['strike_distance']

        # Format expiration date
        exp_date = (datetime.now() + timedelta(days=dte)).strftime('%b %d')

        # Determine target and interpretation
        if direction == "BULLISH":
            target = strike if option_type == "CALL" else "support"
            interpretation = f"Whale betting on upside to ${strike}"
        else:
            target = strike if option_type == "PUT" else "resistance"
            interpretation = f"Whale betting on downside to ${strike}"

        # Individual alerts disabled - only consolidated report sent by analyzer
        # message = (
        #     f"[OPTIONS] {ticker} - {direction} FLOW\n"
        #     f"{signal_type}: ${strike} {option_type}, {exp_date} expiry\n"
        #     f"Premium: ${premium/1000:.0f}K ({volume:,} contracts)\n"
        #     f"Stock: ${stock_price:.2f} -> Target: {strike_distance:+.1f}%\n"
        #     f"Signal: {interpretation}"
        # )
        #
        # self.notifier.send_message(message)

    def run_scan(self, watchlist_only=False, split_mode=None):
        """Run options flow scan

        Args:
            watchlist_only: If True, only scan watchlist stocks (fast mode)
            split_mode: 'priority' = first 300 stocks, 'remaining' = stocks 301+, None = all stocks
        """
        # Determine mode name for display
        if split_mode == "priority":
            mode = "PRIORITY SCAN (Watchlist + First Half)"
        elif split_mode == "remaining":
            mode = "MARKET SCAN (Remaining Stocks)"
        elif watchlist_only:
            mode = "PRIORITY (Watchlist Only)"
        else:
            mode = "Smart Money Scanner"

        print("=" * 50)
        print(f"OPTIONS FLOW TRACKER - {mode}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

        # Load stock universe (priority stocks first, then remaining)
        tickers = self.load_stock_universe()

        # Calculate priority count (from user's watchlist)
        user_watchlist_path = Path("../stock-swing-trader/data/watchlist_all.csv")
        priority_count = 0
        if user_watchlist_path.exists():
            try:
                with open(user_watchlist_path, 'r') as f:
                    priority_count = len([line for line in f.readlines()[1:] if line.strip()])
            except Exception:
                pass

        # Apply split mode filtering
        if split_mode == "priority":
            # Scan first 300 stocks (includes watchlist + first batch of market)
            split_point = min(300, len(tickers))
            tickers = tickers[:split_point]
            print(f"\n[PRIORITY SCAN] Scanning first {len(tickers)} stocks (watchlist priority)...\n")
        elif split_mode == "remaining":
            # Scan stocks from 301 onwards (remaining market stocks)
            split_point = 300
            if len(tickers) > split_point:
                tickers = tickers[split_point:]
                print(f"\n[MARKET SCAN] Scanning remaining {len(tickers)} stocks (stocks #{split_point+1}+)...\n")
            else:
                print(f"\n[MARKET SCAN] No remaining stocks to scan (total universe < {split_point})\n")
                return
        elif watchlist_only and priority_count > 0:
            # Original watchlist-only mode
            tickers = tickers[:priority_count]
            print(f"\n[PRIORITY MODE] Scanning {len(tickers)} watchlist stocks only (fast results)...\n")
        else:
            print(f"\n[SCAN] Scanning {len(tickers)} stocks for unusual flow...\n")

        all_signals = []
        processed = 0
        errors = 0

        for i, ticker in enumerate(tickers, 1):
            # Show separator when switching from priority to remaining stocks
            if i == priority_count + 1 and priority_count > 0:
                print("\n" + "-" * 50)
                print("[SCAN] Completed priority stocks. Scanning remaining market...")
                print("-" * 50 + "\n")

            print(f"[{i}/{len(tickers)}] Scanning {ticker}...", end=" ")

            # Fetch options chain
            chain_data = self.fetch_options_chain(ticker)

            if not chain_data:
                print("No data")
                errors += 1
                continue

            # Analyze for unusual flow
            signals = self.analyze_options_flow(chain_data)

            if signals:
                print(f"OK {len(signals)} signals found")
                all_signals.extend(signals)
            else:
                print("No signals")

            processed += 1

            # Rate limiting to avoid API throttling
            if i % 10 == 0:
                time.sleep(1)

        # Send alerts and log flows
        print(f"\n[ALERTS] Processing {len(all_signals)} signals...\n")

        for signal in all_signals:
            self.log_flow(signal)
            self.send_alert(signal)
            print(f"  OK {signal['ticker']} {signal['signal_type']}: ${signal['premium']/1000:.0f}K")

        # Summary
        print("\n" + "=" * 50)
        print(f"OK Scan complete:")
        print(f"  Processed: {processed} stocks")
        print(f"  Errors: {errors}")
        print(f"  Signals: {len(all_signals)}")
        print("=" * 50)

    def setup_wizard(self):
        """Interactive setup wizard"""
        print("=" * 50)
        print("OPTIONS FLOW TRACKER - Setup Wizard")
        print("=" * 50)

        # Check if stock-swing-trader config exists
        stock_trader_config = Path("../stock-swing-trader/data/config.json")
        if stock_trader_config.exists():
            print("\n[Telegram Configuration]")
            print("Found existing stock-swing-trader config. Reuse credentials? (y/n): ", end="")
            reuse = input().strip().lower()

            if reuse == 'y':
                with open(stock_trader_config, 'r') as f:
                    trader_config = json.load(f)

                self.config['telegram_bot_token'] = trader_config.get('telegram_bot_token')
                self.config['telegram_chat_id'] = trader_config.get('telegram_chat_id')
                print("OK Telegram credentials imported")
            else:
                bot_token = input("Enter Telegram bot token: ").strip()
                chat_id = input("Enter Telegram chat ID: ").strip()
                self.config['telegram_bot_token'] = bot_token
                self.config['telegram_chat_id'] = chat_id
        else:
            print("\n[Telegram Configuration]")
            bot_token = input("Enter Telegram bot token: ").strip()
            chat_id = input("Enter Telegram chat ID: ").strip()
            self.config['telegram_bot_token'] = bot_token
            self.config['telegram_chat_id'] = chat_id

        # Flow detection parameters
        print("\n[Flow Detection Parameters]")
        print("Using recommended defaults for beginners:")
        print(f"  Minimum premium: $50,000 (large institutional trades)")
        print(f"  Sweep threshold: $100,000 (golden sweeps)")
        print(f"  Volume/OI ratio: 5.0x (unusual activity)")
        print(f"  DTE range: 7-45 days (swing trade window)")

        self.config['min_premium'] = 50000
        self.config['sweep_threshold'] = 100000
        self.config['volume_oi_ratio'] = 5.0
        self.config['min_dte'] = 7
        self.config['max_dte'] = 45

        self.save_config()

        print("\nOK Configuration saved to", self.config_path)
        print("\nTesting Telegram connection...")

        notifier = TelegramNotifier(
            self.config['telegram_bot_token'],
            self.config['telegram_chat_id']
        )

        if notifier.send_message("[OPTIONS] Alert System Active"):
            print("OK Telegram test successful!")
        else:
            print("ERROR: Telegram test failed. Check your credentials.")

        print("\n" + "=" * 50)
        print("Setup complete! Run 'python scripts/flow_scanner.py' to start scanning.")
        print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Options Flow Tracker - Smart Money Scanner")
    parser.add_argument('--setup', action='store_true', help='Run setup wizard')
    parser.add_argument('--watchlist-only', action='store_true', help='Scan only watchlist stocks (fast mode)')
    parser.add_argument('--split-mode', choices=['priority', 'remaining'], help='Split scan mode: priority=first 300, remaining=stocks 301+')

    args = parser.parse_args()

    scanner = OptionsFlowScanner()

    if args.setup:
        scanner.setup_wizard()
    else:
        scanner.run_scan(watchlist_only=args.watchlist_only, split_mode=args.split_mode)


if __name__ == "__main__":
    main()
