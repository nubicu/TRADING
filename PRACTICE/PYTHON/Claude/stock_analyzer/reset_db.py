#!/usr/bin/env python3
"""
Reset database and reinitialize with fallback data
"""
import os
import sys
from pathlib import Path

# Change to script directory
os.chdir(Path(__file__).parent)

# Delete database if exists
db_path = 'database.db'
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"✅ Deleted existing database: {db_path}")
    except Exception as e:
        print(f"❌ Error deleting database: {e}")
        sys.exit(1)

# Import after deleting DB
from app import app, db
from models import Stock
from data_fetcher import DataFetcher

print("🔄 Reinitializing database...")

# Create tables
with app.app_context():
    db.create_all()
    print("✅ Created database tables")
    
    # Get initial stock list
    data_fetcher = DataFetcher()
    stock_list = data_fetcher.get_stock_list()
    
    print(f"📊 Loading {len(stock_list)} initial stocks with fallback data...")
    
    from analyzer import StockAnalyzer
    
    for i, (symbol, company_name, sector) in enumerate(stock_list, 1):
        try:
            # Fetch data (will use fallback if API fails)
            data = data_fetcher.fetch_all_data(symbol, company_name)
            
            # Filter data to only include fields that exist in Stock model
            stock_fields = [
                'current_price', 'previous_close', 'daily_change_percent', 'target_price', 'stop_loss',
                'sentiment_score', 'technical_score', 'fundamental_score', 'total_score',
                'news_sentiment', 'social_sentiment', 'market_correlation',
                'rsi', 'macd', 'macd_signal', 'sma_50', 'sma_200', 'volume', 'avg_volume',
                'pe_ratio', 'eps', 'eps_growth', 'peg_ratio', 'revenue_growth', 'debt_to_equity', 'market_cap',
                'sentiment_class', 'recommendation'
            ]
            
            filtered_data = {k: v for k, v in data.items() if k in stock_fields}
            
            # Create stock
            stock = Stock(
                symbol=symbol,
                company_name=company_name,
                sector=sector,
                **filtered_data
            )
            
            # Analyze
            stock = StockAnalyzer.analyze_stock(stock)
            db.session.add(stock)
            
            if i % 50 == 0:
                print(f"  {i}/{len(stock_list)} - {symbol}")
                db.session.commit()
        
        except Exception as e:
            print(f"  ⚠️  Error loading {symbol}: {e}")
            db.session.rollback()
    
    # Final commit
    db.session.commit()
    print(f"✅ Database reset complete with {len(stock_list)} stocks")
    print(f"✅ Now restart Flask app: python app.py")

