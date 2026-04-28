"""
Pulls 2 years of daily FX and commodity prices and saves to data/fx_daily.parquet
(with CSV fallback if pyarrow is unavailable).

Usage:
    python fetch_fx_data.py
"""
import sys
import time
from pathlib import Path

import pandas as pd
import yfinance as yf

FX_COMMODITY = ["AUDUSD=X", "CADUSD=X", "NOKUSD=X", "ZARUSD=X"]
FX_IMPORTER  = ["KRWUSD=X", "IDRUSD=X", "THBUSD=X", "INRUSD=X", "PHPUSD=X"]
COMMODITIES  = ["BZ=F", "GC=F"]
ALL_TICKERS  = FX_COMMODITY + FX_IMPORTER + COMMODITIES


def _normalize_columns(df):
    """yfinance v1.x may return 'AUDUSD=X' or 'AUDUSD' — keep originals if already matching."""
    # Build a map from stripped name back to original ticker
    ticker_map = {t.replace("=X", "").replace("=F", ""): t for t in ALL_TICKERS}
    rename = {}
    for col in df.columns:
        stripped = col.replace("=X", "").replace("=F", "")
        if stripped in ticker_map and col != ticker_map[stripped]:
            rename[col] = ticker_map[stripped]
    if rename:
        df = df.rename(columns=rename)
    return df


def fetch_fx(start="2023-04-01", end=None):
    end = end or pd.Timestamp.today().strftime("%Y-%m-%d")
    print(f"Downloading FX data: {start} → {end} ({len(ALL_TICKERS)} tickers)...")

    try:
        raw = yf.download(ALL_TICKERS, start=start, end=end, auto_adjust=True, progress=False)
    except Exception as e:
        print(f"yfinance download failed: {e}")
        return pd.DataFrame()

    # Extract Close prices from MultiIndex
    if isinstance(raw.columns, pd.MultiIndex):
        df = raw["Close"].copy()
    else:
        df = raw.copy()

    df = _normalize_columns(df)
    df = df.dropna(axis=1, how="all")
    df = df.ffill(limit=5)

    print(f"Downloaded: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    return df


def save_fx(df, data_dir=None):
    if df.empty:
        print("No data to save.")
        return None

    data_dir = data_dir or Path(__file__).parent.parent / "data"
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    try:
        path = data_dir / "fx_daily.parquet"
        df.to_parquet(path)
        print(f"Saved parquet: {path}")
        return str(path)
    except Exception as e:
        print(f"Parquet save failed ({e}) — falling back to CSV")
        path = data_dir / "fx_daily.csv"
        df.to_csv(path)
        print(f"Saved CSV: {path}")
        return str(path)


if __name__ == "__main__":
    df = fetch_fx()
    if not df.empty:
        path = save_fx(df)
        print(f"\nSample (last 3 rows):")
        print(df.tail(3).to_string())
        print(f"\nNaN counts per column:")
        print(df.isna().sum().sort_values())
    else:
        print("Failed to fetch data — check network connection and yfinance tickers.")
        sys.exit(1)
