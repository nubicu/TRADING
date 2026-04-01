from data_fetcher import DataFetcher

f = DataFetcher()
print('Testing MACD comp')
prices = [i+100 for i in range(300)]
macd, signal = f._compute_macd(prices)
print('MACD:', macd, 'Signal:', signal)
print('Technical AAPL')
print(f.fetch_technical_indicators('AAPL'))
