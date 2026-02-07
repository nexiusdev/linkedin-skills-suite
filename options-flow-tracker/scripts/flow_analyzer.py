#!/usr/bin/env python3
"""
Options Flow Analyzer - Smart Alert Screening
Analyzes raw flow signals and generates prioritized recommendations
"""

import sys
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import defaultdict

from telegram_notifier import TelegramNotifier


class FlowAnalyzer:
    def __init__(self, config_path: str = "data/config.json"):
        import json
        self.config_path = Path(config_path)

        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

        self.notifier = TelegramNotifier(
            self.config.get("telegram_bot_token"),
            self.config.get("telegram_chat_id")
        )

        self.flow_log_path = Path("data/flow_history.csv")

    def load_todays_flows(self) -> pd.DataFrame:
        """Load today's flow signals"""
        if not self.flow_log_path.exists():
            return pd.DataFrame()

        df = pd.read_csv(self.flow_log_path)

        # Parse timestamp and filter for today
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        today = datetime.now().date()
        df = df[df['timestamp'].dt.date == today]

        return df

    def calculate_signal_score(self, signal: pd.Series) -> float:
        """Calculate quality score for a single signal (0-100)"""
        score = 0.0

        # 1. Signal type weight (40 points max)
        if signal['signal_type'] == 'Golden Sweep':
            score += 40
        elif signal['signal_type'] == 'Unusual Volume':
            score += 25
        elif signal['signal_type'] == 'Large Block':
            score += 15

        # 2. Premium size (30 points max)
        premium = signal['premium']
        if premium >= 1000000:  # $1M+
            score += 30
        elif premium >= 500000:  # $500K+
            score += 25
        elif premium >= 250000:  # $250K+
            score += 20
        elif premium >= 100000:  # $100K+
            score += 15
        else:  # $50K+
            score += 10

        # 3. Strike distance (20 points max)
        # Closer to current price = higher probability
        strike_dist = abs(signal['strike_distance'])
        if strike_dist <= 5:  # Within 5%
            score += 20
        elif strike_dist <= 10:  # Within 10%
            score += 15
        elif strike_dist <= 20:  # Within 20%
            score += 10
        else:
            score += 5

        # 4. DTE optimization (10 points max)
        # Sweet spot: 14-45 days for swing trades
        dte = signal['expiration_dte']
        if 14 <= dte <= 45:
            score += 10
        elif 7 <= dte < 14 or 45 < dte <= 60:
            score += 7
        elif dte < 7:
            score += 3  # Very short DTE (risky)
        else:
            score += 5

        return score

    def analyze_ticker_cluster(self, ticker: str, signals: pd.DataFrame) -> Dict:
        """Analyze all signals for a single ticker"""

        # Calculate individual signal scores
        signal_scores = signals.apply(self.calculate_signal_score, axis=1)

        # Aggregate metrics
        total_premium = signals['premium'].sum()
        signal_count = len(signals)
        avg_signal_score = signal_scores.mean()

        # Direction analysis
        bullish_count = len(signals[signals['direction'] == 'BULLISH'])
        bearish_count = len(signals[signals['direction'] == 'BEARISH'])

        # Determine consensus direction
        if bullish_count > bearish_count * 1.5:
            consensus = 'BULLISH'
            conviction = bullish_count / signal_count
        elif bearish_count > bullish_count * 1.5:
            consensus = 'BEARISH'
            conviction = bearish_count / signal_count
        else:
            consensus = 'MIXED'
            conviction = 0.5

        # Signal type breakdown
        golden_sweeps = len(signals[signals['signal_type'] == 'Golden Sweep'])
        unusual_volume = len(signals[signals['signal_type'] == 'Unusual Volume'])
        large_blocks = len(signals[signals['signal_type'] == 'Large Block'])

        # Clustering bonus (multiple signals = higher conviction)
        cluster_multiplier = 1.0
        if signal_count >= 10:
            cluster_multiplier = 1.5
        elif signal_count >= 5:
            cluster_multiplier = 1.3
        elif signal_count >= 3:
            cluster_multiplier = 1.15

        # Calculate final conviction score (0-100)
        conviction_score = (avg_signal_score * conviction * cluster_multiplier)

        # Get stock price and key strikes
        stock_price = signals.iloc[0]['stock_price']

        # Find most concentrated strikes
        strike_counts = signals['strike'].value_counts()
        top_strikes = strike_counts.head(3).index.tolist()

        return {
            'ticker': ticker,
            'conviction_score': conviction_score,
            'consensus': consensus,
            'consensus_strength': conviction,
            'signal_count': signal_count,
            'total_premium': total_premium,
            'stock_price': stock_price,
            'golden_sweeps': golden_sweeps,
            'unusual_volume': unusual_volume,
            'large_blocks': large_blocks,
            'top_strikes': top_strikes,
            'bullish_count': bullish_count,
            'bearish_count': bearish_count,
            'signals': signals
        }

    def generate_recommendations(self, df: pd.DataFrame) -> List[Dict]:
        """Generate ranked recommendations from flow data"""

        if df.empty:
            return []

        # Group by ticker
        ticker_analyses = []
        for ticker in df['ticker'].unique():
            ticker_signals = df[df['ticker'] == ticker]
            analysis = self.analyze_ticker_cluster(ticker, ticker_signals)
            ticker_analyses.append(analysis)

        # Sort by conviction score (descending)
        ticker_analyses.sort(key=lambda x: x['conviction_score'], reverse=True)

        return ticker_analyses

    def format_recommendation_report(self, recommendations: List[Dict]) -> str:
        """Format recommendations into a readable report"""

        if not recommendations:
            return "[OPTIONS] No significant flow detected today"

        # Header
        report = f"[OPTIONS FLOW] Daily Recommendation Report\n"
        report += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        report += f"Total tickers with flow: {len(recommendations)}\n"
        report += "=" * 50 + "\n\n"

        # Top 10 highest conviction plays
        top_plays = recommendations[:10]

        for i, rec in enumerate(top_plays, 1):
            ticker = rec['ticker']
            score = rec['conviction_score']
            consensus = rec['consensus']
            signal_count = rec['signal_count']
            total_premium = rec['total_premium']
            stock_price = rec['stock_price']

            # Determine conviction level
            if score >= 70:
                conviction_label = "VERY HIGH"
                emoji = "🔥"
            elif score >= 60:
                conviction_label = "HIGH"
                emoji = "💪"
            elif score >= 50:
                conviction_label = "MODERATE"
                emoji = "👀"
            else:
                conviction_label = "LOW"
                emoji = "⚠️"

            report += f"#{i} {ticker} - {consensus} ({conviction_label} {emoji})\n"
            report += f"Conviction Score: {score:.1f}/100\n"
            report += f"Stock Price: ${stock_price:.2f}\n"
            report += f"Total Premium: ${total_premium/1000:.0f}K ({signal_count} signals)\n"

            # Signal breakdown
            if rec['golden_sweeps'] > 0:
                report += f"  • {rec['golden_sweeps']} Golden Sweep(s)\n"
            if rec['unusual_volume'] > 0:
                report += f"  • {rec['unusual_volume']} Unusual Volume\n"
            if rec['large_blocks'] > 0:
                report += f"  • {rec['large_blocks']} Large Block(s)\n"

            # Direction breakdown
            if consensus == 'MIXED':
                report += f"Direction: Bullish {rec['bullish_count']} | Bearish {rec['bearish_count']}\n"

            # Top concentrated strikes with strategy details
            if rec['top_strikes']:
                strikes_with_strategy = []
                for strike in rec['top_strikes'][:3]:
                    # Find signals with this strike
                    strike_signals = rec['signals'][rec['signals']['strike'] == strike]

                    if not strike_signals.empty:
                        # Get most common DTE for this strike
                        dte = strike_signals['expiration_dte'].mode()[0] if len(strike_signals['expiration_dte'].mode()) > 0 else strike_signals['expiration_dte'].iloc[0]

                        # Determine the predominant strategy for this strike
                        # Count signals by direction and option type
                        strategy_counts = {}
                        for _, sig in strike_signals.iterrows():
                            direction = sig['direction']
                            option_type = sig['option_type']

                            # Infer action (Buy/Sell) from direction + option type
                            # BULLISH + CALL = Buy Call (directional bullish)
                            # BULLISH + PUT = Sell Put (bullish strategy)
                            # BEARISH + CALL = Sell Call (bearish strategy)
                            # BEARISH + PUT = Buy Put (directional bearish)
                            if direction == 'BULLISH' and option_type == 'CALL':
                                action = "Buy Call"
                            elif direction == 'BULLISH' and option_type == 'PUT':
                                action = "Sell Put"
                            elif direction == 'BEARISH' and option_type == 'CALL':
                                action = "Sell Call"
                            elif direction == 'BEARISH' and option_type == 'PUT':
                                action = "Buy Put"
                            else:
                                action = f"{option_type}"

                            strategy_counts[action] = strategy_counts.get(action, 0) + 1

                        # Get the most common strategy
                        dominant_strategy = max(strategy_counts, key=strategy_counts.get)

                        # Format as "$strike Action (Xd)"
                        strikes_with_strategy.append(f"${strike:.0f} {dominant_strategy} ({int(dte)}d)")
                    else:
                        strikes_with_strategy.append(f"${strike:.0f}")

                strikes_str = ", ".join(strikes_with_strategy)
                report += f"Key Strikes: {strikes_str}\n"

            # Generate recommendation
            report += self.generate_action_recommendation(rec) + "\n"
            report += "-" * 50 + "\n\n"

        # Summary stats
        total_premium = sum(r['total_premium'] for r in recommendations)
        total_signals = sum(r['signal_count'] for r in recommendations)

        report += f"SUMMARY:\n"
        report += f"Total Flow Premium: ${total_premium/1000000:.1f}M\n"
        report += f"Total Signals: {total_signals}\n"
        report += f"Top 10 plays shown above\n"

        return report

    def generate_action_recommendation(self, rec: Dict) -> str:
        """Generate detailed, actionable recommendation with specific strategies"""

        ticker = rec['ticker']
        consensus = rec['consensus']
        score = rec['conviction_score']
        stock_price = rec['stock_price']
        total_premium = rec['total_premium']
        golden_sweeps = rec['golden_sweeps']
        top_strikes = rec['top_strikes']
        signals = rec['signals']

        action = ""

        # Mixed signals - wait for clarity
        if consensus == 'MIXED':
            action = f"Action: WAIT - Mixed bullish/bearish signals. "
            action += f"Monitor for directional clarity before entering."
            return action

        # Get average DTE from signals
        avg_dte = int(signals['expiration_dte'].mean()) if not signals.empty else 30

        # Determine signal strength characteristics
        is_massive_premium = total_premium >= 5000000  # $5M+
        is_sweep_heavy = golden_sweeps >= 5
        is_clustered = rec['signal_count'] >= 10

        # Calculate targets and stops based on stock price
        if consensus == 'BULLISH':
            target_1 = stock_price * 1.05  # 5% target
            target_2 = stock_price * 1.10  # 10% target
            stop_loss = stock_price * 0.97  # 3% stop
        else:
            target_1 = stock_price * 0.95  # 5% target (downside)
            target_2 = stock_price * 0.90  # 10% target (downside)
            stop_loss = stock_price * 1.03  # 3% stop (upside)

        # Get recommended strike from top strikes
        rec_strike = top_strikes[0] if top_strikes else stock_price

        # === VERY HIGH CONVICTION (70+) ===
        if score >= 70:
            if consensus == 'BULLISH':
                action = f"💰 STRONG BUY - Institutional accumulation detected.\n"

                # Strategy details
                if is_massive_premium:
                    action += f"   🐋 WHALE ALERT: ${total_premium/1000000:.1f}M premium - Major positioning!\n"

                action += f"   📍 Entry: ${stock_price:.2f} (current price)\n"
                action += f"   🎯 Targets: ${target_1:.2f} (T1), ${target_2:.2f} (T2)\n"
                action += f"   🛑 Stop: ${stock_price * 0.97:.2f} (-3%)\n\n"

                # Strategy options
                action += f"   Strategy Options:\n"
                action += f"   • AGGRESSIVE: Buy ${rec_strike:.0f} calls ({avg_dte}d expiry)\n"
                action += f"   • MODERATE: Buy stock, set {int((target_1-stock_price)/stock_price*100)}% profit target\n"
                action += f"   • CONSERVATIVE: Sell ${int(stock_price * 0.95):.0f} puts, collect premium\n\n"

                # Additional context
                if is_sweep_heavy:
                    action += f"   ⚡ {golden_sweeps} Golden Sweeps = Urgent institutional buying"
                elif is_clustered:
                    action += f"   📊 {rec['signal_count']} signals = High consensus conviction"

            else:  # BEARISH
                action = f"🔴 STRONG SELL/HEDGE - Heavy bearish institutional flow.\n"

                if is_massive_premium:
                    action += f"   🐋 WHALE ALERT: ${total_premium/1000000:.1f}M premium - Major hedging!\n"

                action += f"   📍 Current: ${stock_price:.2f}\n"
                action += f"   🎯 Downside Targets: ${target_1:.2f} (T1), ${target_2:.2f} (T2)\n"
                action += f"   🛑 Risk Limit: ${stock_price * 1.03:.2f} (+3%)\n\n"

                action += f"   Strategy Options:\n"
                action += f"   • AGGRESSIVE: Buy ${rec_strike:.0f} puts ({avg_dte}d expiry)\n"
                action += f"   • MODERATE: Trim/exit longs, raise stops to ${stock_price * 1.02:.2f}\n"
                action += f"   • CONSERVATIVE: Avoid new longs, monitor for reversal\n\n"

                if is_sweep_heavy:
                    action += f"   ⚡ {golden_sweeps} Golden Sweeps = Urgent institutional hedging"
                elif is_clustered:
                    action += f"   📊 {rec['signal_count']} signals = Strong bearish consensus"

        # === HIGH CONVICTION (60-70) ===
        elif score >= 60:
            if consensus == 'BULLISH':
                action = f"📈 BUY SIGNAL - Solid institutional interest.\n"
                action += f"   📍 Entry: ${stock_price:.2f} area\n"
                action += f"   🎯 Target: ${target_1:.2f} (+{int((target_1-stock_price)/stock_price*100)}%)\n"
                action += f"   🛑 Stop: ${stock_price * 0.97:.2f}\n\n"
                action += f"   Recommended: Buy ${rec_strike:.0f} calls or shares on dips"
            else:
                action = f"⚠️ BEARISH SIGNAL - Notable institutional selling.\n"
                action += f"   📍 Current: ${stock_price:.2f}\n"
                action += f"   🎯 Downside: ${target_1:.2f} (-{int((stock_price-target_1)/stock_price*100)}%)\n"
                action += f"   🛑 Avoid: ${stock_price * 1.03:.2f}\n\n"
                action += f"   Recommended: Reduce longs or buy ${rec_strike:.0f} puts for hedge"

        # === MODERATE CONVICTION (50-60) ===
        elif score >= 50:
            if consensus == 'BULLISH':
                action = f"👀 WATCHLIST - Moderate bullish flow detected.\n"
                action += f"   Monitor for entry near ${stock_price * 0.98:.2f} (pullback)\n"
                action += f"   Confirm with price action before entering\n"
                action += f"   Consider: ${rec_strike:.0f} calls if trend confirms"
            else:
                action = f"⚠️ CAUTION - Moderate bearish activity.\n"
                action += f"   Monitor for weakness below ${stock_price * 0.98:.2f}\n"
                action += f"   Tighten stops on existing longs\n"
                action += f"   Wait for clearer direction before shorting"

        # === LOW CONVICTION (<50) ===
        else:
            action = f"ℹ️ INFORMATIONAL - Low conviction signal.\n"
            action += f"   Track for pattern development, no immediate action recommended"

        return action

    def run_analysis(self):
        """Run full analysis and send report"""

        print("=" * 50)
        print("OPTIONS FLOW ANALYZER - Smart Alert Screening")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

        # Load today's flows
        print("\n[LOAD] Reading today's flow signals...")
        df = self.load_todays_flows()

        if df.empty:
            print("No flow signals found for today")
            self.notifier.send_message("[OPTIONS] No significant flow detected today")
            return

        print(f"OK Loaded {len(df)} signals from {df['ticker'].nunique()} tickers")

        # Generate recommendations
        print("\n[ANALYZE] Analyzing flow patterns and clustering...")
        recommendations = self.generate_recommendations(df)
        print(f"OK Generated {len(recommendations)} ticker recommendations")

        # Format report
        print("\n[REPORT] Generating recommendation report...")
        report = self.format_recommendation_report(recommendations)

        # Send via Telegram
        print("\n[SEND] Sending report to Telegram...")

        # Split into chunks if too long (Telegram has 4096 char limit)
        max_length = 4000
        if len(report) <= max_length:
            self.notifier.send_message(report)
            print("OK Report sent successfully")
        else:
            # Split report into chunks
            chunks = []
            current_chunk = ""

            for line in report.split('\n'):
                if len(current_chunk) + len(line) + 1 > max_length:
                    chunks.append(current_chunk)
                    current_chunk = line + '\n'
                else:
                    current_chunk += line + '\n'

            if current_chunk:
                chunks.append(current_chunk)

            print(f"OK Report split into {len(chunks)} messages")
            for i, chunk in enumerate(chunks, 1):
                self.notifier.send_message(chunk)
                print(f"  Sent part {i}/{len(chunks)}")

        # Save detailed analysis to file
        analysis_file = Path("data/daily_analysis.txt")
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nOK Detailed analysis saved to {analysis_file}")

        print("\n" + "=" * 50)
        print("Analysis complete!")
        print("=" * 50)


def main():
    analyzer = FlowAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
