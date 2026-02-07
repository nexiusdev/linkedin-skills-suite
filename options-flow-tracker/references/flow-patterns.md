# Common Options Flow Patterns

Recognizing and interpreting institutional trading patterns.

## Pattern 1: The Golden Sweep

**Definition**: Aggressive buying across multiple strikes with premium $100K+

**Characteristics**:
- High premium ($100K - $1M+)
- Volume 2x+ open interest
- Executes at/near ask (aggressive)
- Often sweeps multiple strikes in succession

**Example**:
```
AAPL $180 Call, Feb 16
Premium: $850K (10,500 contracts @ $8.10)
Volume: 10,500 | OI: 4,200 (2.5x ratio)
Stock: $172.50
```

**Interpretation**:
- **Highest conviction signal**
- Whale willing to pay premium to get filled immediately
- Often precedes significant move
- Time-sensitive (earnings, catalyst expected)

**Trading Action**:
- **Beginner**: Buy stock, set stop at recent support
- **Intermediate**: Buy same-strike calls (smaller size)
- **Advanced**: Match exact position with appropriate risk management

---

## Pattern 2: Unusual Volume Spike

**Definition**: Volume 5x+ open interest, indicating massive new positioning

**Characteristics**:
- Volume significantly exceeds open interest
- Premium $50K+ (institutional size)
- Often at specific strike (cluster)
- May be less aggressive (mid-price fills)

**Example**:
```
TSLA $250 Put, Mar 21
Premium: $320K (4,000 contracts @ $8.00)
Volume: 4,000 | OI: 600 (6.7x ratio)
Stock: $265
```

**Interpretation**:
- New large positions opening (not just churn)
- Strong directional conviction or hedge
- Monitor for continuation
- May be anticipating news/catalyst

**Trading Action**:
- **Bullish flow**: Consider buying stock or calls
- **Bearish flow**: Caution on longs, consider hedging
- **Neutral**: Wait for price confirmation

---

## Pattern 3: Large Block Trade

**Definition**: Single institutional-sized trade $100K+ premium

**Characteristics**:
- Single large execution
- Premium $100K+
- May or may not have unusual volume
- Check bid/ask to determine aggression

**Example**:
```
NVDA $900 Call, Apr 18
Premium: $450K (1,500 contracts @ $30.00)
Volume: 1,500 | OI: 8,500 (0.18x ratio)
Stock: $875
Near ask execution
```

**Interpretation**:
- Institutional player taking position
- If near ask = aggressive/bullish
- If near bid = selling/closing (less bullish)
- Size indicates serious conviction

**Trading Action**:
- Confirm direction (bid vs ask)
- Look for technical confirmation
- Consider scaled entry

---

## Pattern 4: The Straddle/Strangle

**Definition**: Simultaneous large call AND put buying at same or nearby strikes

**Characteristics**:
- Large calls AND puts purchased
- Similar premium on both sides
- Often ATM or near-the-money
- Usually ahead of known catalysts

**Example**:
```
META $450 Call + $450 Put, Jan 25 (earnings)
Call Premium: $280K
Put Premium: $290K
Total: $570K
```

**Interpretation**:
- **Expecting BIG move**, direction unknown
- Common before earnings, FDA decisions, legal rulings
- Not directional - volatility play
- Professional risk management

**Trading Action**:
- **For beginners**: Sit out or small position
- Indicates high volatility expected
- Wait for direction post-catalyst
- Don't fight the implied move

---

## Pattern 5: Calendar Spread

**Definition**: Selling near-term, buying longer-term same strike

**Characteristics**:
- Short front month expiry
- Long back month expiry
- Same strike price
- Moderate premium

**Example**:
```
GOOGL $140 Call
Sold Feb 16 expiry: -2,000 contracts
Bought Mar 21 expiry: +2,000 contracts
```

**Interpretation**:
- Expecting move AFTER near-term expiry
- Reducing theta decay exposure
- Still bullish/bearish but patient
- Professional strategy (less relevant for retail)

**Trading Action**:
- Note the direction (calls = bullish, puts = bearish)
- Timing: expect move in back month window
- Don't necessarily copy this strategy as beginner

---

## Pattern 6: The Hedge

**Definition**: Large put buying in already-owned positions

**Characteristics**:
- Large put volume
- Often 5-10% OTM
- 30-90 DTE common
- May not be truly bearish

**Example**:
```
SPY $550 Put, Mar 21
Premium: $680K (10,000 contracts @ $6.80)
Volume: 10,000 | OI: 15,000
Stock: $600
```

**Interpretation**:
- **May be protective**, not bearish
- Fund hedging long equity exposure
- Risk management, not conviction
- More common during uncertainty

**Trading Action**:
- **Don't blindly follow as bearish**
- Consider market context (VIX, news)
- May actually indicate confidence in longs
- Less actionable than outright bullish/bearish flow

---

## Pattern 7: The Rollout

**Definition**: Closing near-term position, opening same strike further out

**Characteristics**:
- Selling current month
- Buying later month
- Same strike or nearby
- Often in profitable positions

**Example**:
```
MSFT $420 Call
Sold Feb 16: 3,000 contracts (closing)
Bought Mar 21: 3,000 contracts (opening)
```

**Interpretation**:
- Still bullish/bearish, extending time
- Position working but needs more time
- Not closing = still has conviction
- Reducing theta pressure

**Trading Action**:
- Confirms ongoing directional bias
- Note the direction (still positive)
- Lower urgency vs initial entry
- May indicate longer time frame needed

---

## Pattern 8: The Exit

**Definition**: Closing existing positions, reducing exposure

**Characteristics**:
- Selling at bid (liquidating)
- High volume in existing OI
- Volume = or < open interest
- Often near profit targets

**Example**:
```
AAPL $180 Call, Feb 16
Premium: $420K (3,000 contracts @ $14.00)
Volume: 3,000 | OI: 8,000 → 5,000 (OI decreased)
Sold at bid
```

**Interpretation**:
- Profit-taking or cutting losses
- Conviction waning
- Could signal top/bottom
- Contrarian indicator

**Trading Action**:
- **Opposite flow = caution**
- May indicate reversal coming
- Wait for new flow direction
- Consider taking profits if you're in similar trade

---

## Combining Patterns with Technicals

### Bullish Confirmation
- Flow: Large call sweep
- Technical: Breaking resistance
- Volume: Stock volume increasing
- **Action**: High probability long setup

### Bearish Confirmation
- Flow: Large put sweep
- Technical: Breaking support
- Volume: Stock volume increasing
- **Action**: High probability short setup or hedge

### Divergence (Caution)
- Flow: Bullish calls
- Technical: At major resistance
- **Action**: Wait for breakout or skip

### Convergence (Best Setup)
- Flow: Bullish calls
- Technical: Bouncing off support, uptrend intact
- Catalyst: Earnings in 2 weeks
- **Action**: Highest probability setup

---

## Red Flags: When to Ignore Flow

1. **Very short DTE (0-2 days)**
   - Often gamma hedging
   - Market makers adjusting risk
   - Less predictive

2. **Illiquid names**
   - Wide spreads
   - May be individual hedges
   - Less institutional participation

3. **Opposing institutional flow**
   - Golden sweep calls AND puts
   - Directional uncertainty
   - Wait for clarity

4. **Known hedging windows**
   - Month-end rebalancing
   - Quarterly adjustments
   - Less about conviction, more about mechanics

5. **Against strong technical trend**
   - Bearish flow in strong uptrend
   - May be hedging, not conviction
   - Trend > flow

---

## Best Setups for Beginners

### Setup A: Golden Sweep + Technical Breakout
- **Flow**: $100K+ call sweep
- **Chart**: Breaking resistance on volume
- **Action**: Buy stock with stop below breakout

### Setup B: Unusual Volume + Trend Continuation
- **Flow**: 5x+ volume spike in direction of trend
- **Chart**: Pullback to support in uptrend
- **Action**: Enter on bounce

### Setup C: Large Block + Catalyst Ahead
- **Flow**: $200K+ premium, 14-30 DTE
- **Catalyst**: Earnings in 2 weeks
- **Action**: Small position, defined risk

---

## Pattern Recognition Checklist

Before acting on any flow:

- [ ] Premium > $50K (institutional size)
- [ ] Volume/OI ratio > 5x OR Premium > $100K
- [ ] Execution at ask (bullish) or bid (bearish)
- [ ] DTE appropriate (7-45 days ideal)
- [ ] Liquid stock (tight spreads)
- [ ] Technical confirmation
- [ ] Risk defined (stop loss set)
- [ ] Position sized properly (2-5% risk)
