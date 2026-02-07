#!/usr/bin/env python3
"""
Telegram Bot Listener - Receive commands to trigger scans
Supports commands like /scan, /status, /help
"""

import sys
import json
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List


class TelegramBotListener:
    def __init__(self, config_path: str = "data/config.json"):
        self.config_path = Path(config_path)

        if not self.config_path.exists():
            print("ERROR: Config file not found. Run --setup first.")
            sys.exit(1)

        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

        self.bot_token = self.config.get("telegram_bot_token")
        self.chat_id = self.config.get("telegram_chat_id")
        self.last_update_id = 0

        if not self.bot_token or not self.chat_id:
            print("ERROR: Telegram credentials not configured.")
            sys.exit(1)

    def get_updates(self, timeout: int = 30) -> List[Dict]:
        """Get new messages using long polling"""
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"

        params = {
            'offset': self.last_update_id + 1,
            'timeout': timeout,
            'allowed_updates': ['message']
        }

        try:
            response = requests.get(url, params=params, timeout=timeout + 5)
            response.raise_for_status()
            data = response.json()

            if data.get('ok'):
                return data.get('result', [])
            else:
                print(f"Telegram API error: {data}")
                return []

        except requests.RequestException as e:
            print(f"Network error: {e}")
            return []

    def send_message(self, message: str):
        """Send a message back to the user"""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to send message: {e}")

    def handle_scan_command(self) -> str:
        """Trigger options flow scan"""
        self.send_message("🔍 Starting options flow scan...")

        try:
            # Run the daily scan batch file
            script_dir = Path(__file__).parent.parent
            batch_file = script_dir / "run_daily_scan.bat"

            if batch_file.exists():
                result = subprocess.run(
                    [str(batch_file)],
                    capture_output=True,
                    text=True,
                    cwd=str(script_dir),
                    timeout=600  # 10 minute timeout
                )

                if result.returncode == 0:
                    return "✅ Scan completed! Check above for results."
                else:
                    return f"❌ Scan failed with error:\n{result.stderr[:500]}"
            else:
                # Fallback: run Python script directly
                result = subprocess.run(
                    [sys.executable, "scripts/flow_scanner.py"],
                    capture_output=True,
                    text=True,
                    cwd=str(script_dir),
                    timeout=600
                )

                if result.returncode == 0:
                    # Run analyzer
                    subprocess.run(
                        [sys.executable, "scripts/flow_analyzer.py"],
                        cwd=str(script_dir),
                        timeout=60
                    )
                    return "✅ Scan completed! Check above for results."
                else:
                    return f"❌ Scan failed:\n{result.stderr[:500]}"

        except subprocess.TimeoutExpired:
            return "⏱️ Scan timed out (took >10 min). Try again later."
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def handle_status_command(self) -> str:
        """Get scan status"""
        log_file = Path("data/flow_history.csv")

        if not log_file.exists():
            return "📊 No scan data found. Run /scan first."

        try:
            import pandas as pd
            df = pd.read_csv(log_file)

            # Get today's data
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            today = datetime.now().date()
            today_df = df[df['timestamp'].dt.date == today]

            if today_df.empty:
                return "📊 No scans run today yet. Use /scan to start."

            total_signals = len(today_df)
            tickers = today_df['ticker'].nunique()
            total_premium = today_df['premium'].sum()

            last_scan = today_df['timestamp'].max().strftime('%H:%M')

            message = (
                f"📊 <b>Today's Flow Status</b>\n\n"
                f"Last scan: {last_scan}\n"
                f"Signals detected: {total_signals}\n"
                f"Tickers with flow: {tickers}\n"
                f"Total premium: ${total_premium/1000000:.1f}M\n\n"
                f"Use /scan to refresh"
            )

            return message

        except Exception as e:
            return f"❌ Error reading status: {str(e)}"

    def handle_priority_command(self) -> str:
        """Trigger priority scan (watchlist only - fast)"""
        self.send_message("⚡ Starting PRIORITY scan (watchlist only)...")

        try:
            # Run priority scan (watchlist only)
            script_dir = Path(__file__).parent.parent
            batch_file = script_dir / "run_priority_scan.bat"

            if batch_file.exists():
                result = subprocess.run(
                    [str(batch_file)],
                    capture_output=True,
                    text=True,
                    cwd=str(script_dir),
                    timeout=300  # 5 minute timeout (faster than full scan)
                )

                if result.returncode == 0:
                    return "✅ Priority scan completed! Check above for results."
                else:
                    return f"❌ Priority scan failed with error:\n{result.stderr[:500]}"
            else:
                # Fallback: run Python script directly with --watchlist-only flag
                result = subprocess.run(
                    [sys.executable, "scripts/flow_scanner.py", "--watchlist-only"],
                    capture_output=True,
                    text=True,
                    cwd=str(script_dir),
                    timeout=300
                )

                if result.returncode == 0:
                    # Run analyzer
                    subprocess.run(
                        [sys.executable, "scripts/flow_analyzer.py"],
                        cwd=str(script_dir),
                        timeout=60
                    )
                    return "✅ Priority scan completed! Check above for results."
                else:
                    return f"❌ Priority scan failed:\n{result.stderr[:500]}"

        except subprocess.TimeoutExpired:
            return "⏱️ Priority scan timed out (took >5 min). Try again later."
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def handle_help_command(self) -> str:
        """Show available commands"""
        return (
            "🤖 <b>Options Flow Tracker Bot</b>\n\n"
            "<b>Available Commands:</b>\n"
            "/scan - Full scan (314 stocks, ~10 min)\n"
            "/priority - Fast scan (120 watchlist stocks, ~3 min) ⚡\n"
            "/status - Check today's flow stats\n"
            "/help - Show this message\n\n"
            "💡 <b>Quick Start:</b>\n"
            "Send /priority for fast results on your watchlist\n"
            "Send /scan for comprehensive market-wide analysis"
        )

    def process_message(self, message: Dict):
        """Process incoming message"""
        if 'message' not in message:
            return

        msg = message['message']

        # Only respond to messages from the configured chat
        if str(msg['chat']['id']) != str(self.chat_id):
            return

        text = msg.get('text', '').strip().lower()

        if not text:
            return

        # Handle commands
        if text in ['/scan', 'scan', 'run scan', 'start scan', 'full scan']:
            response = self.handle_scan_command()
            # Note: Scan results sent automatically by scanner
            self.send_message(response)

        elif text in ['/priority', 'priority', 'fast scan', 'quick scan']:
            response = self.handle_priority_command()
            # Note: Scan results sent automatically by scanner
            self.send_message(response)

        elif text in ['/status', 'status']:
            response = self.handle_status_command()
            self.send_message(response)

        elif text in ['/help', 'help', '/start']:
            response = self.handle_help_command()
            self.send_message(response)

        else:
            self.send_message(
                f"Unknown command: {text}\n"
                f"Use /help to see available commands"
            )

    def start_listening(self):
        """Start bot listener loop"""
        print("=" * 50)
        print("TELEGRAM BOT LISTENER - Active")
        print(f"Bot Token: {self.bot_token[:20]}...")
        print(f"Chat ID: {self.chat_id}")
        print("=" * 50)
        print("\nListening for commands...")
        print("Press Ctrl+C to stop\n")

        # Send startup notification
        self.send_message("🤖 Options Flow Bot is now active!\nSend /help for commands.")

        try:
            while True:
                updates = self.get_updates()

                for update in updates:
                    self.last_update_id = update['update_id']
                    self.process_message(update)

                # Small delay between polling cycles
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n\nShutting down bot listener...")
            self.send_message("🤖 Options Flow Bot stopped.")
            print("OK Bot stopped")


def main():
    """Start the bot listener"""
    listener = TelegramBotListener()
    listener.start_listening()


if __name__ == "__main__":
    main()
