import sys
sys.path.insert(0, 'E:\\Playground\\PRACTICE\\PYTHON\\Claude\\stock_analyzer')

from data_fetcher import DataFetcher

fetcher = DataFetcher()
print('Testing fetch_essential_data for AAPL...')
essential = fetcher.fetch_essential_data('AAPL', 'Apple Inc.')
print('Essential data keys:', list(essential.keys()))
print('RSI:', essential.get('rsi'))
print('MACD:', essential.get('macd'))
print('SMA50:', essential.get('sma_50'))
print('SMA200:', essential.get('sma_200'))
print('Price:', essential.get('current_price'))
