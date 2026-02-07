"""
Backtesting engine for TraderGPS strategy
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from pathlib import Path

from data_fetcher import fetch_stock_data, fetch_spy_data


class Backtester:
    def __init__(self, config: Dict, aggressive: bool = False):
        self.config = config
        self.aggressive = aggressive
        self.lookback_days = 365  # 1 year

    def check_market_regime(self, spy_data: pd.DataFrame, date_idx: int) -> bool:
        """Check if market was bullish on given date"""
        if date_idx < 50:  # Need 50 days for MA
            return True

        # Calculate 50-day MA up to this date
        historical_data = spy_data.iloc[:date_idx+1]
        ma50 = historical_data['Close'].rolling(window=50).mean().iloc[-1]
        current_close = historical_data['Close'].iloc[-1]

        return current_close > ma50

    def check_buy_signal(self, data: pd.DataFrame, date_idx: int) -> bool:
        """Check if buy signal occurred on given date"""
        if date_idx < 200:  # Need enough data for MA200
            return False

        # Calculate MAs up to this date
        historical_data = data.iloc[:date_idx+1]
        ma20 = historical_data['Close'].rolling(window=20).mean()
        ma50 = historical_data['Close'].rolling(window=50).mean()
        ma200 = historical_data['Close'].rolling(window=200).mean()
        vol_ma20 = historical_data['Volume'].rolling(window=20).mean()

        if len(ma20) < 2 or len(ma50) < 2 or len(ma200) < 1:
            return False

        today = historical_data.iloc[-1]
        yesterday = historical_data.iloc[-2]

        # Filter 1: Minimum Price - Avoid small caps under $10
        min_price = today['Close'] >= 10.0
        if not min_price:
            return False

        # Filter 2: Volatility - Avoid highly volatile stocks (skip in aggressive mode)
        if not self.aggressive:
            # Calculate average daily % change over last 20 days
            daily_returns = historical_data['Close'].pct_change().tail(20)
            avg_daily_move = daily_returns.abs().mean()
            low_volatility = avg_daily_move <= 0.05  # Max 5% average daily move
            if not low_volatility:
                return False

        # Filter 3: Relative Strength - Price must be above 200-day MA
        price_above_ma200 = today['Close'] > ma200.iloc[-1]
        if not price_above_ma200:
            return False

        # Filter 4: Trend Confirmation - 50-day MA must be above 200-day MA
        ma50_above_ma200 = ma50.iloc[-1] > ma200.iloc[-1]
        if not ma50_above_ma200:
            return False

        # Check crossover
        crossover = (ma20.iloc[-1] > ma50.iloc[-1] and
                    ma20.iloc[-2] <= ma50.iloc[-2])

        if not crossover:
            return False

        # Volume requirement - keep at 1.5x for reasonable signals
        volume_spike = today['Volume'] >= (vol_ma20.iloc[-1] * 1.5)

        # Check minimum liquidity
        sufficient_liquidity = vol_ma20.iloc[-1] >= 500_000

        return volume_spike and sufficient_liquidity

    def check_exit_signal(self, data: pd.DataFrame, entry_price: float,
                         entry_idx: int, current_idx: int) -> Tuple[bool, str]:
        """Check if exit signal occurred. Returns (should_exit, reason)"""
        if current_idx <= entry_idx:
            return (False, "")

        # Calculate MAs up to current date
        historical_data = data.iloc[:current_idx+1]
        ma20 = historical_data['Close'].rolling(window=20).mean()
        ma50 = historical_data['Close'].rolling(window=50).mean()

        today = historical_data.iloc[-1]
        current_price = today['Close']

        # Check profit target (+5%)
        if current_price >= entry_price * 1.05:
            return (True, "Profit target")

        # Check stop loss (-3%)
        if current_price <= entry_price * 0.97:
            return (True, "Stop loss")

        # Check MA reversal
        if len(ma20) >= 2 and len(ma50) >= 2:
            yesterday = historical_data.iloc[-2]
            reversal = (ma20.iloc[-1] < ma50.iloc[-1] and
                       ma20.iloc[-2] >= ma50.iloc[-2])
            if reversal:
                return (True, "MA reversal")

        return (False, "")

    def simulate_stock(self, ticker: str, stock_data: pd.DataFrame,
                      spy_data: pd.DataFrame) -> List[Dict]:
        """Simulate trading a single stock over the backtest period"""
        trades = []
        position = None  # Current open position

        for i in range(200, len(stock_data)):  # Start after MA200 warmup period
            current_date = stock_data.index[i]

            # If no position, check for buy signal
            if position is None:
                # Check market regime
                if not self.check_market_regime(spy_data, i):
                    continue

                # Check buy signal
                if self.check_buy_signal(stock_data, i):
                    position = {
                        'ticker': ticker,
                        'entry_date': current_date,
                        'entry_idx': i,
                        'entry_price': stock_data['Close'].iloc[i]
                    }

            # If have position, check for exit signal
            else:
                should_exit, reason = self.check_exit_signal(
                    stock_data,
                    position['entry_price'],
                    position['entry_idx'],
                    i
                )

                if should_exit:
                    exit_price = stock_data['Close'].iloc[i]
                    days_held = (current_date - position['entry_date']).days

                    trade = {
                        'ticker': ticker,
                        'entry_date': position['entry_date'],
                        'entry_price': position['entry_price'],
                        'exit_date': current_date,
                        'exit_price': exit_price,
                        'pnl_pct': ((exit_price - position['entry_price']) /
                                   position['entry_price']) * 100,
                        'pnl_dollars': exit_price - position['entry_price'],
                        'days_held': days_held,
                        'reason': reason
                    }

                    trades.append(trade)
                    position = None  # Close position

        return trades

    def calculate_metrics(self, all_trades: List[Dict]) -> Dict:
        """Calculate performance metrics from trades"""
        if not all_trades:
            return {
                'total_trades': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'profit_factor': 0,
                'total_return': 0,
                'max_drawdown': 0
            }

        df = pd.DataFrame(all_trades)

        wins = df[df['pnl_pct'] > 0]
        losses = df[df['pnl_pct'] <= 0]

        win_count = len(wins)
        loss_count = len(losses)
        win_rate = (win_count / len(df)) * 100 if len(df) > 0 else 0

        avg_win = wins['pnl_pct'].mean() if len(wins) > 0 else 0
        avg_loss = losses['pnl_pct'].mean() if len(losses) > 0 else 0

        gross_profit = wins['pnl_pct'].sum() if len(wins) > 0 else 0
        gross_loss = abs(losses['pnl_pct'].sum()) if len(losses) > 0 else 0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0

        total_return = df['pnl_pct'].sum()

        # Calculate max drawdown (simplified)
        cumulative_returns = df['pnl_pct'].cumsum()
        running_max = cumulative_returns.cummax()
        drawdown = cumulative_returns - running_max
        max_drawdown = drawdown.min() if len(drawdown) > 0 else 0

        return {
            'total_trades': len(df),
            'wins': win_count,
            'losses': loss_count,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'total_return': total_return,
            'max_drawdown': max_drawdown
        }

    def run_backtest(self):
        """Run backtest on watchlist"""
        print("=" * 50)
        print("BACKTESTING - TraderGPS Strategy")
        print(f"Period: Last {self.lookback_days} days (1 year)")
        mode = "AGGRESSIVE" if self.aggressive else "CONSERVATIVE"
        print(f"Mode: {mode} (volatility filter: {'OFF' if self.aggressive else 'ON'})")
        print("=" * 50)

        # Load watchlist
        watchlist_path = self.config.get('watchlist_path')
        if not watchlist_path or not Path(watchlist_path).exists():
            print("\nERROR: Watchlist not found. Run --setup first.")
            return

        with open(watchlist_path, 'r') as f:
            watchlist = [line.strip() for line in f.readlines()[1:] if line.strip()]

        print(f"\nBacktesting {len(watchlist)} stocks...")

        # Fetch SPY data for market regime
        print("Fetching S&P 500 data...")
        spy_data = fetch_spy_data(period="2y")  # Need extra history for MA calculation

        if spy_data is None:
            print("ERROR: Cannot fetch SPY data")
            return

        # Convert SPY index to timezone-naive
        if spy_data.index.tz is not None:
            spy_data.index = spy_data.index.tz_localize(None)

        # Simulate each stock
        all_trades = []

        for ticker in watchlist:
            print(f"Simulating {ticker}...", end=" ")

            stock_data = fetch_stock_data(ticker, period="2y")

            if stock_data is None or len(stock_data) < self.lookback_days:
                print("ERROR: Insufficient data")
                continue

            # Only use last year + 200 days warmup for MA200
            # Convert index to timezone-naive for comparison
            if stock_data.index.tz is not None:
                stock_data.index = stock_data.index.tz_localize(None)

            cutoff_date = datetime.now() - timedelta(days=self.lookback_days)
            stock_data = stock_data[stock_data.index >= cutoff_date - timedelta(days=200)]

            trades = self.simulate_stock(ticker, stock_data, spy_data)
            all_trades.extend(trades)

            print(f"OK {len(trades)} trades")

        # Calculate metrics
        print("\n" + "=" * 50)
        print("BACKTEST RESULTS")
        print("=" * 50)

        metrics = self.calculate_metrics(all_trades)

        print(f"\nTotal trades: {metrics['total_trades']}")
        print(f"Wins: {metrics['wins']} ({metrics['win_rate']:.1f}%)")
        print(f"Losses: {metrics['losses']} ({100 - metrics['win_rate']:.1f}%)")
        print(f"Avg win: +{metrics['avg_win']:.1f}%")
        print(f"Avg loss: {metrics['avg_loss']:.1f}%")
        print(f"Profit factor: {metrics['profit_factor']:.2f}")
        print(f"Max drawdown: {metrics['max_drawdown']:.1f}%")
        print(f"Total return: {metrics['total_return']:+.1f}%")

        # Show sample trades
        if all_trades:
            print("\n" + "=" * 50)
            print("SAMPLE TRADES (Last 5)")
            print("=" * 50)

            df = pd.DataFrame(all_trades)
            recent_trades = df.tail(5)

            for _, trade in recent_trades.iterrows():
                status = "WIN" if trade['pnl_pct'] > 0 else "LOSS"
                print(f"\n[{status}] {trade['ticker']}")
                print(f"  Entry: {trade['entry_date'].strftime('%Y-%m-%d')} @ ${trade['entry_price']:.2f}")
                print(f"  Exit:  {trade['exit_date'].strftime('%Y-%m-%d')} @ ${trade['exit_price']:.2f}")
                print(f"  P&L:   {trade['pnl_pct']:+.1f}% (${trade['pnl_dollars']:+.2f})")
                print(f"  Days:  {trade['days_held']} | Reason: {trade['reason']}")

        print("\n" + "=" * 50)
