# Stock Market Analyzer - Sistem de Analiză și Scoring Acțiuni

## Descriere
Platformă web pentru analiza acțiunilor de pe **NYSE și NASDAQ** bazată pe:
- **Sentiment de piață** (Social media, news, indices)
- **Analiză tehnică** (RSI, MACD, Moving Averages, Volume)
- **Analiză fundamentală** (P/E, EPS, Revenue Growth, Debt Ratio)

Sistem de scoring automat care recomandă acțiuni cu sentiment bullish, inclusiv:
- Preț curent
- Preț țintă
- Stop loss
- Procentaj schimbare zilnică

## 📊 Acoperire Piață

- **NYSE**: 130+ acțiuni din toate sectoarele majore
- **NASDAQ**: 150+ acțiuni tech, biotech, fintech
- **Total**: 280+ acțiuni unice

### Sectoare Acoperite:
✅ Technology & Software  
✅ Financial Services & Fintech  
✅ Healthcare & Biotechnology  
✅ Consumer Goods & Retail  
✅ Energy & Utilities  
✅ Industrials & Manufacturing  
✅ Telecommunications & Media  
✅ Real Estate  
✅ Automotive & Clean Energy  
✅ Entertainment & Gaming

## Caracteristici
✅ Update automat 2x/zi (3h înainte NYSE open + 1h după open)
✅ Bază de date locală SQLite
✅ Dashboard interactiv cu Bootstrap
✅ Grafice interactive
✅ Sistem de alertă pentru oportunități
✅ Filtrare și sortare avansată

## Structura Proiectului
```
stock_analyzer/
├── app.py                 # Flask server principal
├── scheduler.py           # Task scheduler pentru update-uri automate
├── models.py              # Modele bază de date
├── analyzer.py            # Logică scoring și analiză
├── data_fetcher.py        # API calls pentru date financiare
├── requirements.txt       # Dependințe Python
├── database.db            # SQLite database (generat automat)
├── static/
│   ├── css/
│   │   └── style.css      # Stiluri custom
│   └── js/
│       └── main.js        # JavaScript interactiv
├── templates/
│   ├── index.html         # Dashboard principal
│   ├── stock_detail.html  # Detalii acțiune individuală
│   └── settings.html      # Configurări
└── README.md
```

## Instalare

### 1. Instalare dependințe
```bash
pip install -r requirements.txt
```

### 2. Configurare API Keys (opțional - pentru date real-time)
Creați fișier `.env` în root:
```
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

**Nota**: Aplicația funcționează și fără API keys, folosind date simulate pentru demo.

### 3. Pornire aplicație
```bash
# Pornire server Flask
python app.py

# În alt terminal - pornire scheduler
python scheduler.py
```

### 4. Acces aplicație
Deschideți browser la: `http://localhost:5000`

## Programare Update-uri

**NYSE Trading Hours**: 9:30 AM - 4:00 PM EST

**Schedule automat**:
- **Update 1**: 6:30 AM EST (3h înainte de deschidere)
- **Update 2**: 10:30 AM EST (1h după deschidere)

Update-urile includ:
- Preț curent
- Sentiment analysis
- Indicatori tehnici
- Metrici fundamentale
- Recalculare scoring

## Sistem de Scoring

### Formula Generală
```
Total Score = (Sentiment × 35%) + (Technical × 40%) + (Fundamental × 25%)
```

### 1. Sentiment Score (0-100)
- News sentiment: 40%
- Social media mentions: 30%
- Market indices correlation: 30%

### 2. Technical Score (0-100)
- RSI (Relative Strength Index): 25%
- MACD: 25%
- Moving Averages (SMA/EMA): 30%
- Volume trends: 20%

### 3. Fundamental Score (0-100)
- P/E Ratio: 30%
- EPS Growth: 25%
- Revenue Growth: 25%
- Debt-to-Equity: 20%

### Clasificare Sentiment
- **Strong Bullish**: Score > 75
- **Bullish**: Score 60-75
- **Neutral**: Score 40-60
- **Bearish**: Score 25-40
- **Strong Bearish**: Score < 25

## Calculare Preț Țintă și Stop Loss

### Preț Țintă
```
Target Price = Current Price × (1 + Expected Return)
Expected Return = (Technical Score + Fundamental Score) / 200 × Risk Multiplier
```

### Stop Loss
```
Stop Loss = Current Price × (1 - Risk Factor)
Risk Factor = (100 - Total Score) / 100 × 0.15
```

## API Endpoints

### GET /api/stocks
Returnează toate acțiunile cu scoring
```json
{
  "stocks": [...],
  "last_update": "2024-03-25 10:30:00"
}
```

### GET /api/stock/<symbol>
Detalii complete pentru o acțiune
```json
{
  "symbol": "AAPL",
  "current_price": 175.50,
  "target_price": 195.20,
  "stop_loss": 162.30,
  "total_score": 78.5,
  ...
}
```

### POST /api/update
Forțează update manual al datelor
```json
{
  "status": "success",
  "updated_stocks": 50
}
```

## Tehnologii Utilizate
- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite
- **Scheduler**: APScheduler
- **Charts**: Chart.js
- **Icons**: Font Awesome

## Dezvoltare Viitoare
- [ ] Export rapoarte PDF/Excel
- [ ] Alertă email pentru oportunități
- [ ] Machine learning pentru predicții
- [ ] Integrare broker pentru trading automat
- [ ] Mobile app companion

## Licență
MIT License

## Autor
Dezvoltat pentru analiza profesională a piețelor de capital
