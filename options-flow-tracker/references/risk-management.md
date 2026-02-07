# Risk Management for Options Flow Trading

Essential risk rules to protect capital while following institutional flow.

## Core Principle

**Options flow shows conviction, not certainty.** Even whales can be wrong. Risk management is what separates profitable traders from bankrupt ones.

---

## Rule 1: Paper Trade First (1-3 Months)

**Why**: Learn without losing money

**How**:
1. Track all signals in a spreadsheet
2. Log theoretical entry/exit prices
3. Calculate P&L as if you traded
4. Review what worked, what didn't

**Graduation Criteria**:
- 50+ signals tracked
- 60%+ win rate OR positive P&L
- Consistent process
- Understand why signals worked/failed

**Reality Check**: If you can't profit on paper, you won't profit with real money.

---

## Rule 2: Position Sizing (2-5% Per Trade)

**Why**: Protect against catastrophic losses

**How**:
```
Account Size: $10,000
Max Risk Per Trade: 2% = $200
Max Risk Per Trade: 5% = $500 (aggressive)

If stop loss is $2 from entry:
Shares = $200 / $2 = 100 shares maximum
```

**Guidelines**:
- **Conservative (2%)**: Beginner-friendly
- **Moderate (3-4%)**: Some experience required
- **Aggressive (5%)**: Advanced only

**Never**:
- Risk >5% on any single trade
- Compound multiple positions >20% total risk
- Go "all in" on any signal

---

## Rule 3: Use Stop Losses Always

**Why**: Limit losses, let winners run

**How**:

### For Stock Trades (Following Flow)
- **Technical Stop**: Below recent support/swing low
- **Percentage Stop**: 5-8% from entry
- **ATR Stop**: 1.5-2x Average True Range below entry

**Example**:
```
Signal: AAPL bullish call sweep
Stock Entry: $175
Stop Options:
  - Technical: $172 (recent swing low)
  - Percentage: $171 (-2.3%, tight)
  - ATR: $170 (if ATR = $2.50, use 2x = $5 stop)
Choose: $172 (technical makes most sense)
```

### For Options Trades (Directly)
- **Percentage Stop**: 25-50% of premium
- **Time Stop**: Exit if not moving within 3-5 days
- **Technical Stop**: If underlying breaks key level

**Example**:
```
Bought call for $8.00
Stop: $4.00 (50% loss max)
OR
If stock breaks $170 support, exit regardless of option price
```

### Stop Loss Best Practices:
- Set stop BEFORE entering trade
- Use stop-loss orders (not mental stops)
- Don't move stops further away (only closer for profit protection)
- Exit if stop hit, no excuses

---

## Rule 4: Risk/Reward Ratio (Minimum 1:2)

**Why**: Math favors you even with 50% win rate

**How**:
```
Risk: $200 (stop loss)
Reward Target: $400+ (profit target)
Ratio: 1:2

With 50% win rate:
Win: +$400
Loss: -$200
Net: +$200 per 2 trades = +$100 average
```

**Guidelines**:
- **Minimum**: 1:2 risk/reward
- **Good**: 1:3 risk/reward
- **Excellent**: 1:4+ risk/reward

**Before Entry**:
```
Entry: $100
Stop: $95 (risk = $5)
Target: $110+ (reward = $10+)
Ratio: 1:2 ✓ GOOD
```

**Bad Setup**:
```
Entry: $100
Stop: $95 (risk = $5)
Target: $103 (reward = $3)
Ratio: 1:0.6 ✗ BAD (skip this trade)
```

---

## Rule 5: Diversification Limits

**Why**: Don't let one trade wipe you out

**How**:

### Max Exposure per Stock
- **Single stock**: Max 10% of portfolio
- **Single sector**: Max 25% of portfolio
- **Correlated trades**: Count as one exposure

**Example**:
```
Portfolio: $10,000
Max per stock: $1,000
Max per sector (e.g., tech): $2,500

Current positions:
- AAPL: $800 (tech)
- MSFT: $700 (tech)
- GOOGL: Want to enter $1,000 (tech)

Problem: $800 + $700 + $1,000 = $2,500 (at sector limit)
Action: Enter smaller ($500) OR skip
```

### Max Open Positions
- **Beginner**: 2-3 trades max
- **Intermediate**: 5-7 trades max
- **Advanced**: 10+ trades (if properly managed)

---

## Rule 6: Trading Approach by Experience

### Beginner (Recommended)
**Strategy**: Trade underlying stock based on flow

**Why**:
- Less leverage = less risk
- Easier to manage
- Build confidence
- Learn without getting crushed

**Example**:
```
Signal: AAPL $180 call sweep
Your Trade: Buy AAPL stock at $175
Stop: $172
Target: $180+
Risk: Defined, manageable
```

### Intermediate
**Strategy**: Buy calls/puts same direction as flow

**Why**:
- Leverage gains (2-5x)
- Defined risk (can only lose premium)
- Still following the signal

**Example**:
```
Signal: AAPL $180 call sweep
Your Trade: Buy AAPL $180 calls
Stop: -50% on option OR stock breaks support
Target: +100-200% on option
Risk: Higher reward, but can lose 100% of option premium
```

### Advanced
**Strategy**: Match exact strikes/expirations

**Why**:
- Replicate institutional position
- Highest conviction plays
- Requires experience with options Greeks

**Caution**: Only if you understand:
- Implied volatility
- Theta decay
- Gamma risk
- Position sizing with leverage

---

## Rule 7: Time Management

### Entry Timing
- **Flow detected**: Morning scan
- **Technical confirmation**: Wait for setup
- **Entry window**: Generally same day or next day
- **Stale signal**: Skip if flow is >2 days old

### Exit Timing
- **Profit target hit**: Exit 50-75%, let rest run
- **Stop hit**: Exit 100%, no questions
- **No movement**: If dead after 3-5 days, consider exit
- **Catalyst passed**: Exit before/after earnings if that was the thesis

### Time Decay Warning
If trading options directly:
- **0-7 DTE**: Avoid unless advanced (gamma risk)
- **7-14 DTE**: Aggressive, need quick move
- **14-30 DTE**: Moderate, reasonable time
- **30-60 DTE**: Conservative, plenty of time
- **60+ DTE**: LEAPS, very conservative

---

## Rule 8: Never Trade With Emotion

**Emotional Traps**:

### Revenge Trading
- Lost on last trade → desperate to make it back
- **Solution**: Take a break, review what went wrong, stick to system

### FOMO (Fear of Missing Out)
- See big winner after you skipped signal
- **Solution**: There's always another trade, don't chase

### Overconfidence
- Hit 3 winners in a row → get careless
- **Solution**: Every trade still needs proper risk management

### Fear
- Scared to enter after losers
- **Solution**: Trust the process, size down if needed for confidence

**Best Practice**: Follow your rules mechanically, emotions out.

---

## Rule 9: Journaling & Review

**Track Every Trade**:
- Date & ticker
- Signal type (golden sweep, unusual volume, etc.)
- Entry/exit prices
- Stop loss & target
- Outcome (win/loss, % return)
- What worked / what didn't
- Lessons learned

**Weekly Review**:
- Win rate %
- Average win vs average loss
- Best/worst trades
- Pattern recognition (what signals worked best?)
- Mistakes made (how to avoid?)

**Monthly Review**:
- Total P&L
- Sharpe ratio (risk-adjusted return)
- Best performing setups
- What to do more/less of

---

## Rule 10: Know When to Sit Out

**Don't Trade When**:

### Market Conditions
- Extreme volatility (VIX >30)
- Low liquidity (holidays, early close)
- Major uncertainty (geopolitical crisis)

### Personal Conditions
- Emotional (upset, stressed, distracted)
- On losing streak (3+ losses in a row → review system)
- Tired (late at night, after long day)
- Unsure about signal (if in doubt, sit out)

### Signal Quality
- Mixed signals (bullish and bearish flow)
- Low premium (<$50K)
- Illiquid stock (wide spreads)
- Against strong trend (flow counter-trend)

**Remember**: Not trading is a position. Cash is a position. Preservation of capital is priority #1.

---

## Emergency Protocols

### If Down 10% on Position
- Review thesis: still valid?
- Check technical: broken support?
- If thesis broken → exit
- If thesis intact → hold with stop

### If Down 20% on Portfolio
- **STOP TRADING**
- Review last 10 trades
- Identify what went wrong
- Fix the system
- Paper trade until confidence restored

### If Up Big
- Take profits on 25-50% of position
- Raise stops to breakeven
- Let rest run with trailing stop
- Don't get greedy

---

## Position Sizing Calculator

**Formula**:
```
Position Size = (Account Size × Risk %) / (Entry Price - Stop Price)

Example:
Account: $10,000
Risk: 2% = $200
Entry: $100
Stop: $95
Stop Distance: $5

Position Size = $200 / $5 = 40 shares
Total Capital Used: 40 × $100 = $4,000 (40% of account)
```

**Key Point**: Position size ≠ portfolio allocation. You risk $200 (2%), but use $4,000 capital (40%). This is correct because your stop protects you.

---

## The Golden Rules

1. **Never risk more than you can afford to lose**
2. **Losses are part of the game** (win rate will be 50-65%, not 100%)
3. **Protect capital first**, make profits second
4. **Follow the system**, not emotions
5. **There's always another trade** (don't force it)

---

## Beginner Checklist (Before Every Trade)

- [ ] Paper traded successfully (1-3 months)
- [ ] Account size appropriate ($5K+ recommended)
- [ ] Trade size ≤2-5% of account
- [ ] Stop loss defined and set
- [ ] Risk/reward ≥1:2
- [ ] Technical confirmation present
- [ ] Not on emotional tilt
- [ ] Not exceeding exposure limits
- [ ] Journaling prepared
- [ ] Clear thesis (why entering, why exiting)

**If any checkbox is NO → Don't trade.**

---

## Final Thought

> "The goal is not to be right every time. The goal is to make money over time."

Risk management ensures you survive the losses to profit from the wins. Without it, one bad trade can wipe you out. With it, you can trade for years and compound gains.
