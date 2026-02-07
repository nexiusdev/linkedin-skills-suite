#!/usr/bin/env python3
"""
Fetch constituents of major US indices
"""
import yfinance as yf
import requests
import pandas as pd
from io import StringIO

def get_sp500_tickers():
    """Get S&P 500 constituents from Wikipedia"""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        tables = pd.read_html(StringIO(response.text))
        df = tables[0]
        tickers = df['Symbol'].tolist()
        # Clean tickers
        tickers = [t.replace('.', '-') for t in tickers]
        return tickers
    except Exception as e:
        print(f"Error fetching S&P 500: {e}")
        return []

def get_nasdaq100_tickers():
    """Get Nasdaq 100 constituents from Wikipedia"""
    try:
        url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        tables = pd.read_html(StringIO(response.text))
        df = tables[4]  # The constituent table
        tickers = df['Ticker'].tolist()
        tickers = [t.replace('.', '-') for t in tickers]
        return tickers
    except Exception as e:
        print(f"Error fetching Nasdaq 100: {e}")
        return []

def get_dow30_tickers():
    """Get Dow 30 constituents from Wikipedia"""
    try:
        url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        tables = pd.read_html(StringIO(response.text))
        df = tables[1]  # The constituent table
        tickers = df['Symbol'].tolist()
        tickers = [t.replace('.', '-') for t in tickers]
        return tickers
    except Exception as e:
        print(f"Error fetching Dow 30: {e}")
        return []

if __name__ == "__main__":
    print("Fetching major US index constituents...")
    print("=" * 50)

    # Fetch all indices
    sp500 = get_sp500_tickers()
    nasdaq100 = get_nasdaq100_tickers()
    dow30 = get_dow30_tickers()

    print(f"\nS&P 500: {len(sp500)} stocks")
    print(f"Nasdaq 100: {len(nasdaq100)} stocks")
    print(f"Dow 30: {len(dow30)} stocks")

    # Combine and deduplicate
    all_tickers = list(set(sp500 + nasdaq100 + dow30))
    all_tickers.sort()

    print(f"\nTotal unique stocks: {len(all_tickers)}")

    # Save to CSV
    output_file = 'data/watchlist_major_indices.csv'
    with open(output_file, 'w') as f:
        f.write('ticker\n')
        for ticker in all_tickers:
            f.write(f'{ticker}\n')

    print(f"\n✓ Watchlist saved to {output_file}")
    print("\nBreakdown:")
    print(f"  - S&P 500 only: ~{len([t for t in sp500 if t not in nasdaq100 and t not in dow30])}")
    print(f"  - Nasdaq 100 only: ~{len([t for t in nasdaq100 if t not in sp500 and t not in dow30])}")
    print(f"  - Overlap (in 2+ indices): ~{len(sp500) + len(nasdaq100) + len(dow30) - len(all_tickers)}")
