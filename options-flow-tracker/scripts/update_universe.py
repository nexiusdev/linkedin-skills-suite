#!/usr/bin/env python3
"""
Update stock universe to focus on:
1. User's 120 watchlist stocks (priority)
2. Top 194 high-liquidity stocks from major indices (not in watchlist)

Total: ~314 stocks for faster, more actionable scans
"""

import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import datetime

# Comprehensive S&P 500 list (503 stocks)
sp500_tickers = [
    'MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A',
    'APD', 'ABNB', 'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL',
    'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT',
    'AWK', 'AMP', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON', 'APA', 'AAPL',
    'AMAT', 'APTV', 'ACGL', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK',
    'ADP', 'AZO', 'AVB', 'AVY', 'AXON', 'BKR', 'BALL', 'BAC', 'BK', 'BBWI',
    'BAX', 'BDX', 'BBY', 'BIO', 'TECH', 'BIIB', 'BLK', 'BX', 'BA', 'BKNG',
    'BWA', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF-B', 'BLDR', 'BG', 'CDNS',
    'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT',
    'CBOE', 'CBRE', 'CDW', 'CE', 'COR', 'CNC', 'CNP', 'CF', 'CHRW', 'CRL',
    'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO',
    'C', 'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA',
    'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CPAY', 'CTVA',
    'CSGP', 'COST', 'CTRA', 'CRWD', 'CCI', 'CSX', 'CMI', 'CVS', 'DHR', 'DRI',
    'DVA', 'DAY', 'DECK', 'DE', 'DAL', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS',
    'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DHI', 'DTE', 'DUK', 'DD',
    'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'ELV', 'EMR', 'ENPH',
    'ETR', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ERIE', 'ESS', 'EL',
    'ETSY', 'EG', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV',
    'FDS', 'FICO', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FI',
    'FMC', 'F', 'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT',
    'GE', 'GEHC', 'GEV', 'GEN', 'GNRC', 'GD', 'GIS', 'GM', 'GPC', 'GILD',
    'GPN', 'GL', 'GDDY', 'GS', 'HAL', 'HIG', 'HAS', 'HCA', 'DOC', 'HSIC',
    'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM',
    'HPQ', 'HUBB', 'HUM', 'HBAN', 'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'INCY',
    'IR', 'PODD', 'INTC', 'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ',
    'INVH', 'IQV', 'IRM', 'JBHT', 'JBL', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM',
    'JNPR', 'K', 'KVUE', 'KDP', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KKR',
    'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN',
    'LLY', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LULU', 'LYB', 'MTB',
    'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MTCH', 'MKC',
    'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU',
    'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO',
    'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NEM', 'NWSA', 'NWS',
    'NEE', 'NKE', 'NI', 'NDSN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE',
    'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'ON', 'OKE', 'ORCL',
    'OTIS', 'PCAR', 'PKG', 'PLTR', 'PANW', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL',
    'PNR', 'PEP', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PNC', 'POOL', 'PPG',
    'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM',
    'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN',
    'RF', 'RSG', 'RMD', 'RVTY', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI',
    'CRM', 'SBAC', 'SLB', 'STX', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SJM',
    'SW', 'SNA', 'SOLV', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STLD', 'STE',
    'SYK', 'SMCI', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TRGP',
    'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX',
    'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL', 'TSN', 'USB', 'UBER',
    'UDR', 'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR',
    'VLTO', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VTRS', 'VICI', 'V', 'VST', 'VMC',
    'WRB', 'GWW', 'WAB', 'WBA', 'WMT', 'DIS', 'WBD', 'WM', 'WAT', 'WEC',
    'WFC', 'WELL', 'WST', 'WDC', 'WY', 'WMB', 'WTW', 'WYNN', 'XEL', 'XYL',
    'YUM', 'ZBRA', 'ZBH', 'ZTS'
]

# Nasdaq 100 additions (not in S&P 500)
nasdaq_100 = [
    'ADSK', 'ADP', 'ANSS', 'CDNS', 'CHTR', 'CPRT', 'CRWD', 'DXCM', 'FAST',
    'FTNT', 'ILMN', 'INTU', 'ISRG', 'KLAC', 'LRCX', 'MNST', 'MRVL', 'NFLX',
    'NXPI', 'ORLY', 'PAYX', 'PCAR', 'PYPL', 'ROST', 'SNPS', 'TEAM', 'TTWO',
    'VRSK', 'VRTX', 'WBA', 'WDAY', 'XEL', 'ZM', 'ZS'
]

# Dow 30 (all should be in S&P 500 already)
dow_30 = [
    'AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW',
    'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM',
    'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WMT', 'WBA'
]

def load_watchlist():
    """Load user's watchlist from stock-swing-trader"""
    watchlist_path = Path('../stock-swing-trader/data/watchlist_all.csv')

    if not watchlist_path.exists():
        print("⚠️ Watchlist not found at ../stock-swing-trader/data/watchlist_all.csv")
        print("Using empty watchlist")
        return set()

    df = pd.read_csv(watchlist_path)
    watchlist = set(df['ticker'].str.upper())
    print(f'[OK] Loaded {len(watchlist)} stocks from watchlist')
    return watchlist

def get_liquidity_data(tickers, batch_size=50):
    """
    Fetch volume and price data for liquidity ranking
    Returns dict: {ticker: liquidity_score}
    """
    liquidity_scores = {}

    print(f'\nFetching liquidity data for {len(tickers)} stocks...')

    # Process in batches to avoid overwhelming yfinance
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        print(f'  Processing batch {i//batch_size + 1}/{(len(tickers) + batch_size - 1)//batch_size}...', end='')

        try:
            # Download batch data
            data = yf.download(
                batch,
                period='5d',
                progress=False,
                group_by='ticker'
            )

            for ticker in batch:
                try:
                    if len(batch) == 1:
                        # Single ticker - data structure is different
                        ticker_data = data
                    else:
                        # Multiple tickers
                        ticker_data = data[ticker]

                    # Calculate avg volume * avg price as liquidity score
                    avg_volume = ticker_data['Volume'].mean()
                    avg_price = ticker_data['Close'].mean()

                    if pd.notna(avg_volume) and pd.notna(avg_price) and avg_volume > 0:
                        liquidity_scores[ticker] = avg_volume * avg_price

                except Exception as e:
                    # Skip if data unavailable
                    continue

            print(f' [OK] {len([t for t in batch if t in liquidity_scores])} stocks processed')

        except Exception as e:
            print(f' ⚠️ Batch failed: {e}')
            continue

    print(f'[OK] Successfully fetched data for {len(liquidity_scores)} stocks')
    return liquidity_scores

def build_focused_universe():
    """
    Build focused stock universe:
    1. User's 120 watchlist stocks (priority)
    2. Top 194 high-liquidity stocks from indices (not in watchlist)
    """

    print('=' * 60)
    print('BUILDING FOCUSED STOCK UNIVERSE')
    print('=' * 60)

    # Step 1: Load watchlist
    watchlist = load_watchlist()

    # Step 2: Combine all major indices
    all_index_tickers = set(sp500_tickers + nasdaq_100 + dow_30)
    print(f'[OK] Loaded {len(all_index_tickers)} unique stocks from major indices')

    # Step 3: Get non-watchlist stocks for liquidity ranking
    candidates = all_index_tickers - watchlist
    print(f'[OK] {len(candidates)} candidates not in watchlist')

    # Step 4: Fetch liquidity data
    liquidity_scores = get_liquidity_data(list(candidates))

    # Step 5: Rank by liquidity and take top 194
    ranked_candidates = sorted(
        liquidity_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_liquid = [ticker for ticker, score in ranked_candidates[:194]]
    print(f'\n[OK] Selected top 194 most liquid stocks:')
    print(f'   #1: {ranked_candidates[0][0]} (${ranked_candidates[0][1]/1e9:.1f}B daily volume)')
    print(f'   #194: {ranked_candidates[193][0]} (${ranked_candidates[193][1]/1e9:.1f}B daily volume)')

    # Step 6: Combine watchlist + top liquid
    final_universe = list(watchlist) + top_liquid

    # Create dataframe
    df = pd.DataFrame({
        'ticker': final_universe,
        'name': final_universe,
        'index': ['WATCHLIST'] * len(watchlist) + ['LIQUID'] * len(top_liquid)
    })

    # Save
    output_path = Path('assets/stock-universe.csv')
    df.to_csv(output_path, index=False)

    print('\n' + '=' * 60)
    print('UNIVERSE BUILD COMPLETE')
    print('=' * 60)
    print(f'[OK] Watchlist stocks: {len(watchlist)}')
    print(f'[OK] High-liquidity stocks: {len(top_liquid)}')
    print(f'[OK] Total universe: {len(df)} stocks')
    print(f'[OK] Saved to: {output_path}')
    print('=' * 60)

    return df

if __name__ == '__main__':
    build_focused_universe()
