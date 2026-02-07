# TraderGPS Strategy - Detailed Documentation

## Core Philosophy

Colin Seow's TraderGPS strategy combines trend following (moving averages) with momentum confirmation (volume) to identify high-probability swing trade setups. The system is fully objective with no discretionary decisions.

## Entry Logic

### 1. Moving Average Crossover

**Fast MA (20-day)** crosses above **Slow MA (50-day)**

**Calculation:**
- Simple Moving Average (SMA), not exponential
- Both calculated on close prices
- Crossover occurs when: MA20[today] > MA50[today] AND MA20[yesterday] <= MA50[yesterday]

**Why this works:**
- 20-day captures short-term momentum
- 50-day represents intermediate trend
- Crossover signals shift from downtrend to uptrend
- Avoids false signals in choppy, sideways markets

### 2. Volume Confirmation

**Today's volume ≥ 1.5x the 20-day average volume**

**Calculation:**
```
avg_volume_20 = mean(volume of past 20 days)
volume_spike = today's volume >= (avg_volume_20 * 1.5)
```

**Additional filter:**
- Minimum average volume: 500,000 shares/day
- Filters out illiquid stocks with unreliable prices

**Why this works:**
- Volume confirms genuine buying interest
- Large volume prevents false breakouts
- Ensures sufficient liquidity for exits

### 3. Market Regime Filter

**S&P 500 must be above its 50-day MA**

**Calculation:**
- Fetch SPY (S&P 500 ETF) daily close prices
- Calculate 50-day SMA on SPY
- Bullish regime: SPY close > SPY 50-day MA

**Why this works:**
- Tide lifts all boats - trade with the market, not against it
- Significantly reduces losing trades in bear markets
- Improves win rate by 10-15% in historical tests

**Edge case:**
- If SPY data unavailable, default to allowing trades (fail-safe mode)

## Exit Logic

Three independent exit conditions - first one triggered closes the position.

### 1. Profit Target: +5%

**Calculation:**
```
target_price = entry_price * 1.05
exit_triggered = close_price >= target_price
```

**Execution:**
- Exit at close price on the day target is reached
- No intraday exits (EOD data only)

### 2. Stop Loss: -3%

**Calculation:**
```
stop_price = entry_price * 0.97
exit_triggered = close_price <= stop_price
```

**Risk management:**
- Risk/reward ratio: 1.67 (5% gain / 3% loss)
- Protects capital on losing trades
- No "hoping it comes back" - systematic cut losses

### 3. Trend Reversal

**20-day MA crosses below 50-day MA**

**Calculation:**
- MA20[today] < MA50[today] AND MA20[yesterday] >= MA50[yesterday]

**Rationale:**
- Original uptrend has ended
- Even if not yet at profit target, exit to avoid giving back gains
- Protects against slow erosion in sideways markets

**Edge case:**
- If already in profit when reversal occurs, exit immediately
- If in loss and approaching stop loss, stop loss takes precedence

## Position Sizing

**Current implementation:**
- Equal weight across all positions
- Maximum 10 simultaneous positions (one per watchlist stock)
- No position pyramiding or averaging down

**Future enhancements:**
- Volatility-based sizing using ATR
- Kelly criterion position sizing
- Risk-based allocation (fixed % of capital per trade)

## Earnings Handling

**Detection:**
- Check earnings calendar API (if available)
- Flag positions with earnings within 7 days

**Action:**
- System provides warning in daily update
- No automatic exit - user decides
- Recommendation: Close positions 1-2 days before earnings to avoid gap risk

**Rationale:**
- Earnings create volatility outside normal technical analysis
- Gap moves can bypass stop losses
- Conservative approach: avoid earnings risk

## Historical Performance Expectations

Based on Colin Seow's published results and similar MA crossover strategies:

**Expected metrics:**
- Win rate: 55-70%
- Average win: 4-6%
- Average loss: 2-3%
- Profit factor: 1.8-2.5
- Max drawdown: 10-15%
- Annual return: 15-25% (market dependent)

**Best conditions:**
- Trending bull markets
- Low volatility environments
- Sectors with strong momentum

**Worst conditions:**
- Choppy, sideways markets
- High volatility / whipsaw conditions
- Bear markets (market regime filter helps here)

## Edge Cases and Handling

### Gap Openings

**Scenario:** Stock gaps up/down on open, bypassing targets

**Handling:**
- EOD data only, so exit at close price
- If gap bypasses profit target: exit at close (may get >5% gain)
- If gap bypasses stop loss: exit at close (may lose >3%)

**Mitigation:**
- Avoid holding through earnings (reduces gap risk)
- Accept that gaps are part of swing trading

### Low Liquidity Days

**Scenario:** Volume drops significantly after entry

**Handling:**
- No liquidity filter after entry
- Exit signals still trigger normally
- User responsible for actual execution liquidity

### Multiple Signals Same Day

**Scenario:** Multiple stocks trigger buy signals simultaneously

**Handling:**
- Rank by volume spike strength (higher = better)
- Take top signals up to position limit
- Log rejected signals for reference

### Simultaneous Exit Signals

**Scenario:** Both profit target AND MA reversal trigger same day

**Handling:**
- Profit target takes priority
- Record exit reason as "Profit target"
- Academic distinction - both indicate exit

## Strategy Modifications Not Recommended

**Don't change:**
- Moving average periods (20/50 is well-tested)
- Profit/loss ratio (5%/3% balances win rate and reward)
- Volume multiplier (1.5x is sweet spot)

**Optional enhancements:**
- ATR-based stops (more adaptive than fixed %)
- Trailing stops (lock in profits as price runs)
- Sector rotation (focus on strongest sectors)
- Relative strength ranking (trade strongest stocks only)

## Limitations and Risks

**This strategy will NOT:**
- Catch the absolute bottom or top
- Work in all market conditions
- Eliminate losing trades
- Provide daily income (positions may last weeks)

**This strategy DOES:**
- Follow trends systematically
- Cut losses quickly
- Let winners run to target
- Remove emotional decision-making
- Provide clear entry/exit rules

## Recommended Usage

**Time commitment:**
- 10-15 minutes daily for scanning and monitoring
- Weekly watchlist review and rotation

**Capital requirements:**
- Minimum $10,000 to properly diversify across 10 positions
- Each position: ~10% of capital

**Skill level:**
- Beginner friendly (systematic rules)
- No discretion required
- Clear signals and alerts

**Realistic expectations:**
- Not a get-rich-quick system
- Steady, systematic gains over time
- Some losing trades are normal and expected
- Follow the rules consistently for best results
