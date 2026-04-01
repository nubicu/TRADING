# Ghid de Customizare - Stock Market Analyzer

## 🎯 Adăugare Acțiuni Noi

### Metoda 1: Editare Directă în `data_fetcher.py`

```python
# Deschide data_fetcher.py și modifică lista DEMO_STOCKS:

DEMO_STOCKS = [
    # Simbolul, Numele Companiei, Sectorul
    ('AAPL', 'Apple Inc.', 'Technology'),
    ('MSFT', 'Microsoft Corporation', 'Technology'),
    
    # Adaugă acțiunile tale aici:
    ('ROKU', 'Roku Inc.', 'Technology'),
    ('SQ', 'Block Inc.', 'Financial'),
    ('SHOP', 'Shopify Inc.', 'Technology'),
    ('COIN', 'Coinbase Global', 'Financial'),
    
    # ... restul acțiunilor
]
```

### Metoda 2: Import din CSV

Creează `custom_stocks.csv`:
```csv
symbol,company_name,sector
ROKU,Roku Inc.,Technology
SQ,Block Inc.,Financial
SHOP,Shopify Inc.,Technology
```

Apoi modifică `data_fetcher.py`:
```python
import csv

def load_custom_stocks():
    stocks = []
    try:
        with open('custom_stocks.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stocks.append((
                    row['symbol'],
                    row['company_name'],
                    row['sector']
                ))
    except FileNotFoundError:
        pass
    return stocks

# În __init__ sau get_stock_list():
self.DEMO_STOCKS.extend(load_custom_stocks())
```

---

## ⚙️ Ajustare Weights pentru Scoring

### Modificare în `analyzer.py`

```python
class StockAnalyzer:
    # Weights originale:
    SENTIMENT_WEIGHT = 0.35    # 35%
    TECHNICAL_WEIGHT = 0.40    # 40%
    FUNDAMENTAL_WEIGHT = 0.25  # 25%
    
    # Exemplu: Dacă preferi focus pe Technical:
    # SENTIMENT_WEIGHT = 0.25    # 25%
    # TECHNICAL_WEIGHT = 0.50    # 50%
    # FUNDAMENTAL_WEIGHT = 0.25  # 25%
    
    # Sau focus pe Fundamental (value investing):
    # SENTIMENT_WEIGHT = 0.20    # 20%
    # TECHNICAL_WEIGHT = 0.30    # 30%
    # FUNDAMENTAL_WEIGHT = 0.50  # 50%
```

### Ajustare Sub-Weights

```python
@staticmethod
def calculate_sentiment_score(stock):
    # Originale:
    news_weight = 0.40
    social_weight = 0.30
    market_weight = 0.30
    
    # Customizează aici:
    # news_weight = 0.50    # Mai mult focus pe știri
    # social_weight = 0.20
    # market_weight = 0.30
```

---

## 🎨 Customizare Interfață

### Schimbare Culori în `static/css/style.css`

```css
/* La începutul fișierului, modifică variabilele: */

:root {
    --primary-color: #0d6efd;      /* Albastru - schimbă cu #6f42c1 pentru violet */
    --success-color: #198754;      /* Verde pentru bullish */
    --danger-color: #dc3545;       /* Roșu pentru bearish */
    --warning-color: #ffc107;      /* Galben pentru warning */
    
    /* Dark mode (exemplu):
    --primary-color: #4dabf7;
    --success-color: #51cf66;
    --danger-color: #ff6b6b;
    */
}
```

### Schimbare Logo/Brand

```html
<!-- În templates/index.html, modifică navbar-brand: -->

<a class="navbar-brand" href="/">
    <i class="fas fa-chart-line"></i> Numele Tău
</a>

<!-- Sau adaugă logo imagine: -->
<a class="navbar-brand" href="/">
    <img src="/static/img/logo.png" height="30"> Stock Analyzer
</a>
```

---

## 📊 Customizare Clasificare Scoruri

### În `analyzer.py`, funcția `classify_sentiment`:

```python
@staticmethod
def classify_sentiment(total_score):
    """Clasifică sentimentul bazat pe scor"""
    
    # Clasificare originală:
    if total_score >= 75:
        return 'Strong Bullish', 'BUY'
    elif total_score >= 60:
        return 'Bullish', 'BUY'
    elif total_score >= 40:
        return 'Neutral', 'HOLD'
    elif total_score >= 25:
        return 'Bearish', 'SELL'
    else:
        return 'Strong Bearish', 'SELL'
    
    # Clasificare mai conservatoare (exemplu):
    # if total_score >= 80:
    #     return 'Strong Bullish', 'BUY'
    # elif total_score >= 65:
    #     return 'Bullish', 'BUY'
    # elif total_score >= 35:
    #     return 'Neutral', 'HOLD'
    # elif total_score >= 20:
    #     return 'Bearish', 'SELL'
    # else:
    #     return 'Strong Bearish', 'SELL'
```

---

## 🎯 Ajustare Risk Management

### Target Price și Stop Loss în `analyzer.py`

```python
class StockAnalyzer:
    # Risk multipliers originale:
    RISK_MULTIPLIER = 1.5         # Pentru target price
    MAX_STOP_LOSS_PERCENT = 0.15  # 15% max stop loss
    
    # Mai agresiv (trading activ):
    # RISK_MULTIPLIER = 2.0
    # MAX_STOP_LOSS_PERCENT = 0.20
    
    # Mai conservator (value investing):
    # RISK_MULTIPLIER = 1.0
    # MAX_STOP_LOSS_PERCENT = 0.10
```

### Customizare Formula Target Price

```python
@staticmethod
def calculate_target_price(stock, total_score):
    # Formula originală
    tech_fund_avg = (stock.technical_score + stock.fundamental_score) / 2
    expected_return = (tech_fund_avg / 100) * StockAnalyzer.RISK_MULTIPLIER
    
    # Exemplu customizat - include și sentiment:
    # all_scores_avg = (stock.sentiment_score + stock.technical_score + stock.fundamental_score) / 3
    # expected_return = (all_scores_avg / 100) * StockAnalyzer.RISK_MULTIPLIER
    
    # Bonus pentru sentiment foarte bullish
    if total_score > 75:
        expected_return *= 1.2
    
    # Customizare: bonus mai mare
    # if total_score > 80:
    #     expected_return *= 1.5
    # elif total_score > 70:
    #     expected_return *= 1.3
    
    target_price = stock.current_price * (1 + expected_return)
    return round(target_price, 2)
```

---

## 🔔 Adăugare Notificări Email

### 1. Instalează dependency
```bash
pip install flask-mail
```

### 2. Adaugă în `app.py`

```python
from flask_mail import Mail, Message

# Configurare email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'

mail = Mail(app)

def send_alert(stock):
    """Trimite email pentru oportunități bullish"""
    if stock.total_score >= 75:
        msg = Message(
            f'🚀 Strong Bullish Alert: {stock.symbol}',
            sender='your-email@gmail.com',
            recipients=['destination@example.com']
        )
        msg.body = f"""
        Acțiune: {stock.symbol} - {stock.company_name}
        
        Total Score: {stock.total_score}
        Sentiment: {stock.sentiment_class}
        
        Preț Curent: ${stock.current_price}
        Preț Țintă: ${stock.target_price}
        Stop Loss: ${stock.stop_loss}
        
        Upside Potential: {((stock.target_price - stock.current_price) / stock.current_price * 100):.1f}%
        """
        
        try:
            mail.send(msg)
            print(f"✉️  Email sent for {stock.symbol}")
        except Exception as e:
            print(f"❌ Email failed: {e}")
```

### 3. Call în `trigger_update` după analyze

```python
# După StockAnalyzer.analyze_stock(stock)
send_alert(stock)
```

---

## 📈 Adăugare Export Date

### Export CSV

Adaugă endpoint nou în `app.py`:

```python
import csv
from io import StringIO
from flask import make_response

@app.route('/api/export/csv')
def export_csv():
    """Export acțiuni în CSV"""
    stocks = Stock.query.order_by(Stock.total_score.desc()).all()
    
    # Create CSV
    si = StringIO()
    writer = csv.writer(si)
    
    # Header
    writer.writerow([
        'Symbol', 'Company', 'Sector', 'Current Price', 'Target Price',
        'Stop Loss', 'Total Score', 'Sentiment', 'Technical', 'Fundamental',
        'Classification', 'Recommendation'
    ])
    
    # Data
    for stock in stocks:
        writer.writerow([
            stock.symbol,
            stock.company_name,
            stock.sector,
            stock.current_price,
            stock.target_price,
            stock.stop_loss,
            stock.total_score,
            stock.sentiment_score,
            stock.technical_score,
            stock.fundamental_score,
            stock.sentiment_class,
            stock.recommendation
        ])
    
    # Create response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=stocks.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output
```

Apoi în `index.html`, adaugă buton:
```html
<a href="/api/export/csv" class="btn btn-success">
    <i class="fas fa-download"></i> Export CSV
</a>
```

---

## 🌓 Dark Mode

### Adaugă în `static/css/style.css`

```css
/* Dark mode variables */
body.dark-mode {
    background-color: #1a1a1a;
    color: #e0e0e0;
}

body.dark-mode .card {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

body.dark-mode .table {
    color: #e0e0e0;
}

body.dark-mode .table thead th {
    background-color: #1a1a1a;
    border-color: #444;
}

body.dark-mode .navbar {
    background-color: #000 !important;
}
```

### Toggle în `main.js`

```javascript
// Dark mode toggle
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load saved preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}
```

Apoi adaugă buton în navbar (`index.html`):
```html
<button class="btn btn-outline-light btn-sm" onclick="toggleDarkMode()">
    <i class="fas fa-moon"></i>
</button>
```

---

## 🔧 Debugging și Logging

### Adaugă logging detaliat în `app.py`

```python
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
if not app.debug:
    file_handler = RotatingFileHandler('stock_analyzer.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Stock Analyzer startup')

# În funcții, folosește:
app.logger.info(f'Stock {symbol} analyzed: score={stock.total_score}')
app.logger.error(f'Error fetching {symbol}: {str(e)}')
```

---

## 📱 Adăugare PWA (Progressive Web App)

### 1. Creează `static/manifest.json`

```json
{
  "name": "Stock Market Analyzer",
  "short_name": "Stock Analyzer",
  "description": "AI-powered stock analysis platform",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0d6efd",
  "icons": [
    {
      "src": "/static/img/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/img/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 2. Adaugă în `<head>` în toate template-urile

```html
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#0d6efd">
```

---

## 🚀 Performance Optimization

### 1. Cache API Responses

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache pentru 5 minute
@lru_cache(maxsize=128)
def get_cached_stocks(timestamp):
    # timestamp schimbat la fiecare 5 min
    return Stock.query.all()

@app.route('/api/stocks')
def get_stocks():
    # Cache key se schimbă la fiecare 5 min
    cache_key = datetime.now().replace(second=0, microsecond=0)
    cache_key = cache_key - timedelta(minutes=cache_key.minute % 5)
    
    stocks = get_cached_stocks(cache_key.timestamp())
    # ...
```

### 2. Database Indexing

```python
# În models.py, adaugă indices:

class Stock(db.Model):
    # ... existing fields ...
    
    __table_args__ = (
        db.Index('idx_total_score', 'total_score'),
        db.Index('idx_sentiment_class', 'sentiment_class'),
        db.Index('idx_sector', 'sector'),
    )
```

---

**Customizează după nevoile tale! 🎨**
