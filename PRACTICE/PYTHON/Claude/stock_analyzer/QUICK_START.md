# Quick Start Guide - Stock Market Analyzer

## 🚀 Pornire Rapidă (5 minute)

### Pașii Esențiali

#### 1️⃣ Instalare Dependințe
```bash
cd stock_analyzer
pip install -r requirements.txt
```

#### 2️⃣ Pornire Server
```bash
python app.py
```

#### 3️⃣ Acces Dashboard
Deschide browser: **http://localhost:5000**

---

## 📊 Ce Face Aplicația?

### Analizează Automat Acțiuni Bazat Pe:
1. **📰 Sentiment** (35%) - News, Social Media, Market Trends
2. **📈 Technical** (40%) - RSI, MACD, Moving Averages, Volume
3. **💰 Fundamental** (25%) - P/E, EPS, Revenue Growth, Debt

### Recomandări Automate:
- ✅ **Preț Curent** - Valoarea actuală pe piață
- 🎯 **Preț Țintă** - Unde poate ajunge
- 🛑 **Stop Loss** - Limită de risc
- 📊 **Scor Total** - 0-100 (mai mare = mai bullish)
- 💡 **Sentiment** - Strong Bullish → Strong Bearish

---

## ⏰ Update-uri Automate

### Program NYSE
- **6:30 AM EST** - Pre-market update (3h înainte de deschidere)
- **10:30 AM EST** - Post-open update (1h după deschidere)

### Pentru Update-uri Automate
```bash
# În terminal separat
python scheduler.py
```

---

## 🎯 Interfața Web

### 1. Dashboard Principal (`/`)
- **Cards cu statistici**: Bullish, Neutral, Bearish, Average Score
- **Filtre**: Sentiment, Sector, Score minim
- **Sortare**: După score, preț, schimbare zilnică
- **Tabel complet**: Toate acțiunile cu detalii

### 2. Detalii Acțiune (`/stock/SYMBOL`)
- **Score-uri detaliate**: Sentiment, Technical, Fundamental
- **Target Price & Stop Loss**
- **Grafice interactive**: Istoric preț și score (30 zile)
- **Indicatori tehnici**: RSI, MACD, SMA 50/200
- **Metrici fundamentale**: P/E, EPS, Market Cap

### 3. Settings (`/settings`)
- **Informații sistem**: Schedule, Scoring formula
- **Manual update**: Trigger forțat pentru date noi
- **Recent updates log**: Istoric actualizări

---

## 🔍 Exemple de Utilizare

### Găsire Oportunități Bullish
1. Du-te la Dashboard
2. Setează **Sentiment Filter**: "Strong Bullish" sau "Bullish"
3. Setează **Min Score**: 60
4. Sortează după **Total Score** descrescător
5. Click pe simbolul acțiunii pentru detalii complete

### Analiză Tehnică Detaliată
1. Click pe simbolul acțiunii (ex: AAPL)
2. Vezi graficele de preț și score
3. Verifică RSI (< 30 = oversold, > 70 = overbought)
4. Compară SMA 50 vs SMA 200 (Golden/Death Cross)

### Monitorizare Portofoliu
1. Folosește **Search**: introdu simbolurile tale
2. Verifică **Daily Change %** pentru performance
3. Compară **Current Price** vs **Target Price** pentru upside
4. Verifică **Stop Loss** pentru managementul riscului

---

## 📱 API Endpoints (Pentru Dezvoltatori)

### GET `/api/stocks`
```bash
curl "http://localhost:5000/api/stocks?min_score=60&sentiment=Bullish"
```

### GET `/api/stock/AAPL`
```bash
curl "http://localhost:5000/api/stock/AAPL"
```

### POST `/api/update`
```bash
curl -X POST http://localhost:5000/api/update \
  -H "Content-Type: application/json" \
  -d '{"update_type": "manual"}'
```

### GET `/api/stats`
```bash
curl "http://localhost:5000/api/stats"
```

---

## 🎨 Interpretare Scoruri

### Total Score
| Range | Classification | Badge Color | Action |
|-------|---------------|-------------|--------|
| 75-100 | Strong Bullish | 🟢 Green | **BUY** |
| 60-75 | Bullish | 🔵 Blue | **BUY** |
| 40-60 | Neutral | ⚪ Gray | **HOLD** |
| 25-40 | Bearish | 🟡 Yellow | **SELL** |
| 0-25 | Strong Bearish | 🔴 Red | **SELL** |

### Indicatori Tehnici

**RSI (Relative Strength Index)**
- < 30: Oversold (posibil cumpărare)
- 30-70: Normal range
- > 70: Overbought (posibil vânzare)

**MACD**
- MACD > Signal: Bullish (trend ascendent)
- MACD < Signal: Bearish (trend descendent)

**Moving Averages**
- Price > SMA 50 > SMA 200: Strong uptrend
- SMA 50 > SMA 200: Golden Cross (bullish)
- SMA 50 < SMA 200: Death Cross (bearish)

---

## ⚡ Tips & Tricks

### 1. Update Rapid
Click butonul **Refresh** din navbar pentru date recente

### 2. Multi-Sort
Combină filtrele pentru găsirea exactă:
- Sentiment: "Bullish" + Min Score: 70 + Sector: "Technology"

### 3. Keyboard Shortcuts
- Folosește **Search** pentru găsire rapidă după simbol
- Tab pentru navigare între filtre

### 4. Mobile Friendly
Dashboard-ul e responsive - funcționează perfect pe telefon

---

## 🐛 Troubleshooting Rapid

### ❌ "No stocks found"
**Soluție**: 
```bash
# Trigger manual update
curl -X POST http://localhost:5000/api/update
```
Sau click "Trigger Manual Update" în Settings

### ❌ Port 5000 ocupat
**Soluție**: Schimbă portul în `app.py` (ultima linie):
```python
app.run(debug=True, port=5001)  # Folosește 5001
```

### ❌ Database error
**Soluție**:
```bash
rm database.db
python app.py  # Recreează database
```

---

## 🔐 Securitate & Date

### Date Simulate (Demo Mode)
- Aplicația funcționează **fără API keys**
- Folosește date realiste simulate
- Perfect pentru testare și învățare

### Date Real-Time (Producție)
1. Obține API keys gratuit:
   - Alpha Vantage: https://www.alphavantage.co/support/#api-key
   - News API: https://newsapi.org/register

2. Creează fișier `.env`:
```bash
cp .env.example .env
nano .env  # Adaugă keys
```

3. Restart aplicația

---

## 📚 Resurse Suplimentare

- **README.md**: Documentație completă
- **INSTALL.md**: Ghid detaliat de instalare
- **app.py**: Comentarii în cod pentru API
- **analyzer.py**: Logică scoring explicată

---

## 💡 Următorii Pași

### Nivel Beginner
1. ✅ Explorează dashboard-ul
2. ✅ Verifică câteva acțiuni populare (AAPL, MSFT, GOOGL)
3. ✅ Înțelege scoring-ul

### Nivel Intermediate
1. ✅ Configurează update-uri automate
2. ✅ Experimentează cu filtrele
3. ✅ Analizează graficele istorice

### Nivel Advanced
1. ✅ Integrează API keys reale
2. ✅ Customizează scoring weights (în `analyzer.py`)
3. ✅ Configurează pentru producție (vezi INSTALL.md)
4. ✅ Adaugă mai multe acțiuni (în `data_fetcher.py`)

---

## 🆘 Suport

Dacă întâmpini probleme:
1. Verifică secțiunea **Troubleshooting** mai sus
2. Citește **INSTALL.md** pentru setup detaliat
3. Verifică logs în terminal pentru erori

---

**Enjoy analyzing! 📈📊💹**
