"""
Telegram notification utilities
"""

import requests
from typing import Optional


class TelegramNotifier:
    def __init__(self, bot_token: Optional[str], chat_id: Optional[str]):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.enabled = bool(bot_token and chat_id)

    def send_message(self, message: str) -> bool:
        """
        Send a message via Telegram

        Args:
            message: Message text to send

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            print(f"[Telegram disabled] {message}")
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Telegram error: {e}")
            return False


def main():
    """Test Telegram connection"""
    import sys
    import json
    from pathlib import Path

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        config_path = Path("data/config.json")

        if not config_path.exists():
            print("ERROR: Config file not found. Run --setup first.")
            sys.exit(1)

        with open(config_path, 'r') as f:
            config = json.load(f)

        notifier = TelegramNotifier(
            config.get('telegram_bot_token'),
            config.get('telegram_chat_id')
        )

        if notifier.send_message("Stock Trader Alert System Active"):
            print("OK Test message sent successfully!")
        else:
            print("ERROR: Failed to send test message")
            sys.exit(1)
    else:
        print("Usage: python telegram_notifier.py --test")


if __name__ == "__main__":
    main()
