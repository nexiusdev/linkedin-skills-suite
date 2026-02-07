# Telegram Bot Setup Guide

This guide walks through setting up a Telegram bot for receiving stock trading alerts.

## Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow prompts to name your bot (e.g., "Stock Trader Alerts")
4. BotFather will provide a **bot token** - save this (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Get Your Chat ID

**Option A: Using your bot**
1. Send any message to your new bot in Telegram
2. Visit this URL in your browser (replace `YOUR_BOT_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Look for `"chat":{"id":123456789` - that number is your chat ID

**Option B: Using @userinfobot**
1. Search for `@userinfobot` in Telegram
2. Start a chat - it will reply with your chat ID

## Step 3: Configure the Skill

When you run `python scripts/trader.py --setup`, you'll be prompted to enter:

1. **Telegram Bot Token**: Paste the token from BotFather
2. **Telegram Chat ID**: Enter your chat ID from Step 2

These credentials are saved to `data/config.json` (keep this file private).

## Step 4: Test Your Setup

Send a test message:

```bash
python scripts/telegram_notifier.py --test
```

You should receive a message: "🔔 Stock Trader Alert System Active"

If you don't receive the message:
- Verify bot token and chat ID are correct
- Ensure you've sent at least one message to your bot first
- Check for typos in config.json

## Using Group Chats (Optional)

To receive alerts in a Telegram group:

1. Create a group in Telegram
2. Add your bot to the group
3. Make the bot an admin (required for sending messages)
4. Get the group chat ID:
   - Send a message in the group
   - Visit `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
   - Look for `"chat":{"id":-123456789` (negative number for groups)
5. Use this negative number as your chat ID in config

## Alert Customization

By default, alerts are sent for:
- ✅ New buy signals
- ✅ Exit signals (profit target, stop loss, MA reversal)
- ✅ Daily position updates

To modify alert behavior, edit the `telegram_notifier.py` script.

## Privacy and Security

**Important:**
- Keep your bot token private - it controls your bot
- Don't share `data/config.json` publicly
- If token is compromised, use BotFather to regenerate it (`/revoke`)

**Bot token is NOT sensitive financial information:**
- It only allows sending messages to your chat
- Cannot access your Telegram account
- Cannot access trading platforms or finances

## Troubleshooting

**"Chat not found" error:**
- Ensure you've messaged the bot first
- For groups, ensure bot is added and is an admin

**"Unauthorized" error:**
- Bot token is incorrect
- Check for extra spaces or typos

**Messages not arriving:**
- Check bot wasn't blocked
- Verify chat ID is correct (positive for DMs, negative for groups)
- Ensure internet connection is stable

**Rate limiting:**
- Telegram allows ~30 messages per second
- This skill sends max 1 message per stock event
- Rate limiting unlikely unless scanning 100+ stocks
