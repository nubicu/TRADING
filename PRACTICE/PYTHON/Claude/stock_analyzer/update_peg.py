#!/usr/bin/env python3
"""
Update PEG ratios for all existing stocks
"""
import os
import sys
from pathlib import Path

# Change to script directory
os.chdir(Path(__file__).parent)

# Import after changing directory
from app import app, db
from models import Stock
from data_fetcher import DataFetcher

print("🔄 Updating PEG ratios for all stocks...")

data_fetcher = DataFetcher()

with app.app_context():
    stocks = Stock.query.all()
    updated_count = 0

    for stock in stocks:
        try:
            # Fetch fundamental data
            fund_data = data_fetcher.fetch_fundamental_data(stock.symbol)

            # Update PEG ratio if available
            if 'peg_ratio' in fund_data and fund_data['peg_ratio'] is not None:
                stock.peg_ratio = fund_data['peg_ratio']
                updated_count += 1
                print(f"  Updated {stock.symbol}: PEG = {stock.peg_ratio}")

            # Also update other fundamental data
            for key, value in fund_data.items():
                if hasattr(stock, key) and value is not None:
                    setattr(stock, key, value)

        except Exception as e:
            print(f"  ⚠️  Error updating {stock.symbol}: {e}")

    # Commit all changes
    db.session.commit()
    print(f"✅ Updated PEG ratios for {updated_count}/{len(stocks)} stocks")