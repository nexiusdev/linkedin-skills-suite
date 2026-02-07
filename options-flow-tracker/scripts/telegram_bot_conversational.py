#!/usr/bin/env python3
"""
Conversational Telegram Bot - Answer questions about options flow
Supports natural language queries about stocks, flow analysis, and trading advice
"""

import sys
import json
import time
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List


class ConversationalFlowBot:
    def __init__(self, config_path: str = "data/config.json"):
        self.config_path = Path(config_path)

        if not self.config_path.exists():
            print("ERROR: Config file not found.")
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

    def load_todays_analysis(self) -> Optional[str]:
        """Load today's flow analysis report"""
        analysis_file = Path("data/daily_analysis.txt")

        if not analysis_file.exists():
            return None

        # Check if file is from today
        mod_time = datetime.fromtimestamp(analysis_file.stat().st_mtime)
        if mod_time.date() != datetime.now().date():
            return None

        with open(analysis_file, 'r') as f:
            return f.read()

    def load_todays_flow(self) -> Optional[pd.DataFrame]:
        """Load today's flow signals"""
        flow_file = Path("data/flow_history.csv")

        if not flow_file.exists():
            return None

        try:
            df = pd.read_csv(flow_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Get today's data
            today = datetime.now().date()
            today_df = df[df['timestamp'].dt.date == today]

            return today_df if not today_df.empty else None

        except Exception as e:
            print(f"Error loading flow data: {e}")
            return None

    def get_stock_flow(self, ticker: str) -> str:
        """Get flow analysis for a specific stock"""
        ticker = ticker.upper()

        # Load today's analysis first
        analysis = self.load_todays_analysis()
        if analysis and ticker in analysis:
            # Extract the relevant section
            lines = analysis.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('#') and ticker in line:
                    # Get this stock's section
                    section = []
                    for j in range(i, min(i+10, len(lines))):
                        if lines[j].startswith('--'):
                            break
                        section.append(lines[j])
                    return '\n'.join(section)

        # Fallback: Query raw flow data
        df = self.load_todays_flow()
        if df is None:
            return f"❌ No flow data available for today. Run /scan first."

        stock_df = df[df['ticker'] == ticker]
        if stock_df.empty:
            return f"📊 No unusual flow detected for {ticker} today."

        total_premium = stock_df['premium'].sum()
        signal_count = len(stock_df)

        # Determine direction
        calls = stock_df[stock_df['option_type'] == 'call']
        puts = stock_df[stock_df['option_type'] == 'put']

        call_premium = calls['premium'].sum() if not calls.empty else 0
        put_premium = puts['premium'].sum() if not puts.empty else 0

        direction = "BULLISH" if call_premium > put_premium else "BEARISH"

        message = (
            f"📊 <b>{ticker} Flow Analysis</b>\n\n"
            f"Direction: <b>{direction}</b>\n"
            f"Total Premium: ${total_premium/1000:.0f}K\n"
            f"Signals: {signal_count}\n"
            f"  • Calls: ${call_premium/1000:.0f}K\n"
            f"  • Puts: ${put_premium/1000:.0f}K\n\n"
            f"💡 {direction} flow suggests institutional {direction.lower()} positioning."
        )

        return message

    def handle_question(self, text: str) -> str:
        """Answer natural language questions about flow"""
        text_lower = text.lower()

        # Extract ticker if mentioned
        words = text.upper().split()
        potential_tickers = [w for w in words if len(w) <= 5 and w.isalpha()]

        # Check for specific ticker query
        if any(keyword in text_lower for keyword in ['flow on', 'about', 'what about', 'check', 'analyze']):
            for ticker in potential_tickers:
                if len(ticker) >= 1:
                    return self.get_stock_flow(ticker)

        # Check for direct ticker mention
        if len(potential_tickers) == 1:
            return self.get_stock_flow(potential_tickers[0])

        # Generic questions
        if 'report' in text_lower or 'summary' in text_lower or 'top' in text_lower:
            analysis = self.load_todays_analysis()
            if analysis:
                # Return first 1000 chars
                return f"📊 <b>Today's TOP 10 Flow Report:</b>\n\n{analysis[:1000]}...\n\nSee full report above ☝️"
            else:
                return "❌ No analysis available yet. Run /scan first."

        if 'help' in text_lower or 'what can' in text_lower:
            return self.get_help_message()

        # Default: Try to extract ticker from message
        if potential_tickers:
            return self.get_stock_flow(potential_tickers[0])

        return (
            "🤔 I can help you with:\n\n"
            "• Ask about specific stocks: <i>\"What's the flow on MSFT?\"</i>\n"
            "• Get today's report: <i>\"Show me the summary\"</i>\n"
            "• Run scans: /scan or /priority\n"
            "• Check status: /status\n\n"
            "Just mention a ticker or ask a question!"
        )

    def get_help_message(self) -> str:
        """Show help message"""
        return (
            "🤖 <b>Options Flow Bot - Conversational Mode</b>\n\n"
            "<b>Commands:</b>\n"
            "/scan - Full market scan (~10 min)\n"
            "/priority - Fast watchlist scan (~3 min) ⚡\n"
            "/status - Today's flow stats\n"
            "/help - Show this message\n\n"
            "<b>Ask Questions:</b>\n"
            "• \"What's the flow on MSFT?\"\n"
            "• \"Should I buy NVDA?\"\n"
            "• \"AAPL analysis\"\n"
            "• \"Show me today's report\"\n"
            "• \"What about CRM?\"\n\n"
            "💡 Just mention a ticker or ask a question - I'll help you analyze the flow!"
        )

    def process_message(self, message: Dict):
        """Process incoming message"""
        if 'message' not in message:
            return

        msg = message['message']

        # Only respond to messages from the configured chat
        if str(msg['chat']['id']) != str(self.chat_id):
            return

        text = msg.get('text', '').strip()

        if not text:
            return

        # Handle basic commands
        text_lower = text.lower()

        if text_lower in ['/help', 'help']:
            self.send_message(self.get_help_message())

        elif text_lower in ['/status', 'status']:
            df = self.load_todays_flow()
            if df is None:
                self.send_message("📊 No scan data today. Run /scan to start.")
            else:
                total_signals = len(df)
                tickers = df['ticker'].nunique()
                total_premium = df['premium'].sum()
                last_scan = df['timestamp'].max().strftime('%H:%M')

                msg_text = (
                    f"📊 <b>Today's Flow Status</b>\n\n"
                    f"Last scan: {last_scan}\n"
                    f"Signals: {total_signals}\n"
                    f"Tickers: {tickers}\n"
                    f"Premium: ${total_premium/1000000:.1f}M"
                )
                self.send_message(msg_text)

        else:
            # Natural language processing
            response = self.handle_question(text)
            self.send_message(response)

    def run(self):
        """Main bot loop"""
        print("="*50)
        print("CONVERSATIONAL OPTIONS FLOW BOT")
        print("="*50)
        print(f"Bot listening for messages...")
        print(f"Chat ID: {self.chat_id}")
        print("Send /help to see available commands")
        print("Press Ctrl+C to stop")
        print("="*50)

        self.send_message("🤖 <b>Conversational Flow Bot Started!</b>\n\nAsk me questions about options flow!\nType /help for commands.")

        while True:
            try:
                updates = self.get_updates()

                for update in updates:
                    self.last_update_id = update['update_id']
                    self.process_message(update)

            except KeyboardInterrupt:
                print("\n\nBot stopped by user")
                self.send_message("🛑 Bot stopped.")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(5)


if __name__ == "__main__":
    bot = ConversationalFlowBot()
    bot.run()
