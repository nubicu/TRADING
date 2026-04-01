#!/usr/bin/env python3
"""Test news relevance filtering"""
from data_fetcher import DataFetcher

fetcher = DataFetcher()

# Test with multiple symbols
test_symbols = [
    ('AAPL', 'Apple Inc.'),
    ('GOOGL', 'Alphabet Inc.'),
    ('TSLA', 'Tesla Inc.')
]

print("=" * 70)
print("🧪 Testing News Relevance Filtering")
print("=" * 70)

for symbol, company_name in test_symbols:
    print(f"\n📍 Testing {symbol} ({company_name})")
    print("-" * 70)
    
    sentiment_data = fetcher.fetch_sentiment_data(symbol, company_name)
    articles = sentiment_data.get('news_articles', [])
    
    print(f"📰 Found {len(articles)} articles")
    
    for i, article in enumerate(articles[:3], 1):
        title = article.get('title', '')
        source = article.get('source', 'Unknown')
        
        # Check if title contains symbol or company name
        title_lower = title.lower()
        symbol_in_title = symbol.lower() in title_lower
        company_in_title = company_name.lower() in title_lower
        is_relevant = symbol_in_title or company_in_title
        
        print(f"\n  {i}. [{source}] {title[:80]}...")
        print(f"     ✓ Contains '{symbol}': {symbol_in_title}")
        print(f"     ✓ Contains '{company_name}': {company_in_title}")
        print(f"     🎯 Relevant: {is_relevant}")

print("\n" + "=" * 70)
print("✅ Test Complete")
print("=" * 70)
