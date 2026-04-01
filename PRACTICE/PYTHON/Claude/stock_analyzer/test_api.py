import requests
r = requests.get('http://localhost:5000/api/stock/AAPL')
print('status', r.status_code)
print('keys', r.json().keys())
stock = r.json().get('stock', {})
print('stock RSI', stock.get('rsi'))
print('news count', len(r.json().get('news', [])))
