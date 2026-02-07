"""
Data fetching utilities for stock and market data
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


def fetch_stock_data(ticker: str, period: str = "6mo") -> Optional[pd.DataFrame]:
    """
    Fetch historical stock data from Yahoo Finance

    Args:
        ticker: Stock ticker symbol
        period: Data period (default: 6mo for 6 months)

    Returns:
        DataFrame with OHLCV data, or None if fetch fails
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)

        if data.empty:
            return None

        return data

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None


def fetch_spy_data(period: str = "6mo") -> Optional[pd.DataFrame]:
    """
    Fetch S&P 500 (SPY) data for market regime check

    Args:
        period: Data period (default: 6mo)

    Returns:
        DataFrame with SPY data, or None if fetch fails
    """
    return fetch_stock_data("SPY", period)


def get_earnings_date(ticker: str) -> Optional[datetime]:
    """
    Get next earnings date for a stock

    Args:
        ticker: Stock ticker symbol

    Returns:
        datetime of next earnings, or None if not available
    """
    try:
        stock = yf.Ticker(ticker)
        calendar = stock.calendar

        if calendar is None or calendar.empty:
            return None

        # Try to get earnings date from calendar
        if 'Earnings Date' in calendar.index:
            earnings_date = calendar.loc['Earnings Date'].iloc[0]

            if pd.notna(earnings_date):
                # Convert to datetime if it's not already
                if isinstance(earnings_date, str):
                    earnings_date = pd.to_datetime(earnings_date)
                return earnings_date

        return None

    except Exception:
        # Earnings date not available or error occurred
        return None


def calculate_sma(data: pd.DataFrame, window: int, column: str = 'Close') -> pd.Series:
    """
    Calculate Simple Moving Average

    Args:
        data: DataFrame with price data
        window: Moving average window (e.g., 20, 50)
        column: Column name to calculate SMA on (default: Close)

    Returns:
        Series with SMA values
    """
    return data[column].rolling(window=window).mean()


def calculate_volume_average(data: pd.DataFrame, window: int = 20) -> pd.Series:
    """
    Calculate average volume over a window

    Args:
        data: DataFrame with volume data
        window: Window period (default: 20)

    Returns:
        Series with volume average
    """
    return data['Volume'].rolling(window=window).mean()


def is_crossover(fast: pd.Series, slow: pd.Series) -> bool:
    """
    Check if fast line crossed above slow line on most recent bar

    Args:
        fast: Fast moving average series
        slow: Slow moving average series

    Returns:
        True if crossover occurred, False otherwise
    """
    if len(fast) < 2 or len(slow) < 2:
        return False

    # Today: fast > slow
    # Yesterday: fast <= slow
    return (fast.iloc[-1] > slow.iloc[-1] and
            fast.iloc[-2] <= slow.iloc[-2])


def is_crossunder(fast: pd.Series, slow: pd.Series) -> bool:
    """
    Check if fast line crossed below slow line on most recent bar

    Args:
        fast: Fast moving average series
        slow: Slow moving average series

    Returns:
        True if crossunder occurred, False otherwise
    """
    if len(fast) < 2 or len(slow) < 2:
        return False

    # Today: fast < slow
    # Yesterday: fast >= slow
    return (fast.iloc[-1] < slow.iloc[-1] and
            fast.iloc[-2] >= slow.iloc[-2])
