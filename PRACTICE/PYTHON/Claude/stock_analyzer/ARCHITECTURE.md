# Arhitectura Aplicației - Stock Market Analyzer

## 📐 Overview Arhitectural

### Stack Tehnologic

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                        │
│  HTML5 + CSS3 + Bootstrap 5 + JavaScript + Chart.js    │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   BACKEND LAYER (Flask)                  │
│  Python 3.8+ │ Flask │ SQLAlchemy │ APScheduler         │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC                         │
│  StockAnalyzer │ DataFetcher │ Scoring Engine           │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   DATA LAYER                             │
│  SQLite Database │ Stock Models │ History               │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   EXTERNAL APIs (Optional)               │
│  Alpha Vantage │ News API │ Social Media APIs           │
└─────────────────────────────────────────────────────────┘
```

---

## 🏗️ Componente Principale

### 1. **app.py** - Flask Application Server

**Responsabilități:**
- Inițializare server Flask
- Definire routes și API endpoints
- Gestiune sesiuni și requests
- Orchestrare între componente

**Endpoints Principale:**
```python
GET  /                    # Dashboard principal
GET  /stock/<symbol>      # Detalii acțiune
GET  /settings           # Pagină setări

GET  /api/stocks         # Lista acțiuni cu filtre
GET  /api/stock/<symbol> # Detalii + istoric
GET  /api/sectors        # Sectoare disponibile
POST /api/update         # Trigger update manual
GET  /api/stats          # Statistici generale
GET  /api/history/<sym>  # Istoric grafice
```

**Flow Diagram:**
```
Request → Flask Router → Business Logic → Database
                                ↓
                         Response (JSON/HTML)
```

---

### 2. **models.py** - Database Models

**Schema Database:**

#### Tabel: `stocks`
```sql
├── id (PK)
├── symbol (UNIQUE, INDEXED)
├── company_name
├── sector
│
├── current_price
├── previous_close
├── daily_change_percent
├── target_price
├── stop_loss
│
├── sentiment_score
├── technical_score
├── fundamental_score
├── total_score
│
├── news_sentiment
├── social_sentiment
├── market_correlation
│
├── rsi
├── macd
├── macd_signal
├── sma_50
├── sma_200
├── volume
├── avg_volume
│
├── pe_ratio
├── eps
├── eps_growth
├── revenue_growth
├── debt_to_equity
├── market_cap
│
├── sentiment_class
├── recommendation
│
├── last_updated
└── created_at
```

#### Tabel: `update_logs`
```sql
├── id (PK)
├── update_type (pre_market/post_open/manual)
├── start_time
├── end_time
├── stocks_updated
├── status
├── error_message
└── created_at
```

#### Tabel: `stock_history`
```sql
├── id (PK)
├── stock_id (FK → stocks.id)
├── price
├── total_score
├── volume
└── recorded_at (INDEXED)
```

**Relații:**
```
Stock (1) ←→ (Many) StockHistory
```

---

### 3. **analyzer.py** - Scoring Engine

**Algoritm de Scoring:**

```
┌──────────────────────────────────────────────┐
│         SENTIMENT SCORE (0-100)              │
│  News: 40% + Social: 30% + Market: 30%       │
└──────────────────────────────────────────────┘
                    ↓ × 35%
┌──────────────────────────────────────────────┐
│         TECHNICAL SCORE (0-100)              │
│  RSI: 25% + MACD: 25% + MA: 30% + Vol: 20%   │
└──────────────────────────────────────────────┘
                    ↓ × 40%
┌──────────────────────────────────────────────┐
│        FUNDAMENTAL SCORE (0-100)             │
│  P/E: 30% + EPS: 25% + Rev: 25% + Debt: 20%  │
└──────────────────────────────────────────────┘
                    ↓ × 25%
┌──────────────────────────────────────────────┐
│              TOTAL SCORE                     │
│    = Weighted Sum of All Components          │
└──────────────────────────────────────────────┘
```

**Funcții Principale:**

1. **calculate_sentiment_score()**
   - Input: Stock object cu date sentiment
   - Output: Score 0-100
   - Logic: Normalizare + weighted average

2. **calculate_technical_score()**
   - Input: Stock cu indicatori tehnici
   - Output: Score 0-100
   - Logic: 
     - RSI: < 30 = oversold (100), > 70 = overbought (0)
     - MACD: > Signal = bullish
     - MA: Golden Cross = bullish
     - Volume: > Average = strong signal

3. **calculate_fundamental_score()**
   - Input: Stock cu metrici fundamentale
   - Output: Score 0-100
   - Logic:
     - P/E: < 15 = undervalued (100)
     - EPS Growth: > 20% = excellent (100)
     - Revenue Growth: > 15% = strong (100)
     - Debt-to-Equity: < 0.5 = very low debt (100)

4. **calculate_target_price()**
   ```python
   Expected Return = (Technical + Fundamental) / 200 × Risk Multiplier
   
   if Total Score > 75:
       Expected Return × 1.2  # Bonus bullish
   
   Target = Current Price × (1 + Expected Return)
   ```

5. **calculate_stop_loss()**
   ```python
   Risk Factor = (100 - Total Score) / 100 × 0.15
   Risk Factor = max(Risk Factor, 0.05)  # Min 5%
   
   Stop Loss = Current Price × (1 - Risk Factor)
   ```

---

### 4. **data_fetcher.py** - Data Acquisition

**Dual Mode Operation:**

```
┌─────────────────────────────────────────────┐
│  API Keys Present?                          │
└─────────────────────────────────────────────┘
         │
         ├─── YES → REAL-TIME MODE
         │          │
         │          ├─ Alpha Vantage (Price Data)
         │          ├─ News API (Sentiment)
         │          └─ Calculate Technicals
         │
         └─── NO  → DEMO MODE
                    │
                    └─ Simulated Realistic Data
```

**Data Flow:**

```
fetch_all_data(symbol)
    ├─→ fetch_price_data()
    │      └─→ current_price, previous_close, volume
    │
    ├─→ fetch_technical_indicators()
    │      └─→ RSI, MACD, SMA, avg_volume
    │
    ├─→ fetch_fundamental_data()
    │      └─→ P/E, EPS, revenue_growth, debt
    │
    └─→ fetch_sentiment_data()
           └─→ news_sentiment, social, correlation
```

**Funcții de Simulare:**
- `_generate_demo_price_data()`: Prețuri realiste bazate pe simboluri
- `_generate_demo_technical_data()`: Indicatori în range-uri normale
- `_generate_demo_fundamental_data()`: Metrici fundamentale variabile
- `_generate_demo_sentiment_data()`: Sentiment cu bias realistic

---

### 5. **scheduler.py** - Automated Updates

**Scheduling Architecture:**

```
┌──────────────────────────────────────────────┐
│         APScheduler Background               │
└──────────────────────────────────────────────┘
              │
              ├─→ CronTrigger: 6:30 AM EST
              │   └─→ pre_market_update()
              │       └─→ POST /api/update
              │
              └─→ CronTrigger: 10:30 AM EST
                  └─→ post_open_update()
                      └─→ POST /api/update
```

**Timezone Handling:**
```python
EST = pytz.timezone('America/New_York')
Current Server Time → Convert to EST → Check Schedule
```

**Update Flow:**
```
Scheduler Trigger
    ↓
HTTP POST to Flask /api/update
    ↓
For each stock:
    ├─ Fetch fresh data
    ├─ Update stock object
    ├─ Calculate scores
    ├─ Save to database
    └─ Log to history
    ↓
Log update result
    ↓
Return statistics
```

---

## 🔄 Data Flow Complet

### Update Cycle:

```
1. TRIGGER (Scheduler sau Manual)
   ↓
2. FETCH DATA pentru fiecare stock
   ├─ Price data
   ├─ Technical indicators
   ├─ Fundamental metrics
   └─ Sentiment data
   ↓
3. DATABASE UPDATE
   └─ Update sau Create stock record
   ↓
4. SCORING ENGINE
   ├─ Calculate Sentiment Score
   ├─ Calculate Technical Score
   ├─ Calculate Fundamental Score
   └─ Calculate Total Score
   ↓
5. PRICE TARGETS
   ├─ Calculate Target Price
   └─ Calculate Stop Loss
   ↓
6. CLASSIFICATION
   └─ Assign Sentiment Class & Recommendation
   ↓
7. HISTORY SNAPSHOT
   └─ Save to stock_history table
   ↓
8. LOG UPDATE
   └─ Record in update_logs
```

### User Request Flow:

```
Browser Request
   ↓
Flask Route Handler
   ↓
Query Database
   ↓
Format Response (JSON/HTML)
   ↓
Return to Browser
   ↓
JavaScript Rendering
   └─ Update DOM + Charts
```

---

## 🎨 Frontend Architecture

### Template Hierarchy:

```
base.html (concept - poate fi implementat)
   ├─ index.html (Dashboard)
   ├─ stock_detail.html (Individual Stock)
   └─ settings.html (Settings Page)
```

### JavaScript Modules:

**main.js:**
```javascript
├─ loadStocks()           // Fetch și display toate acțiunile
├─ loadSectors()          // Populate sector filter
├─ loadStats()            // Dashboard statistics
├─ renderStocksTable()    // Render tabel HTML
├─ applyFilters()         // Client-side filtering
├─ setupFilters()         // Event listeners
└─ refreshData()          // Forțează reload
```

**stock_detail.html (inline):**
```javascript
├─ loadStockDetails()     // Fetch detalii stock
├─ renderStockDetails()   // Render HTML
├─ createPriceChart()     // Chart.js pentru preț
└─ createScoreChart()     // Chart.js pentru score
```

### CSS Organization:

```css
style.css
   ├─ :root variables        // Color scheme
   ├─ General styles          // Body, navigation
   ├─ Stat cards             // Dashboard cards
   ├─ Tables                 // Stock listing
   ├─ Score badges           // Color coding
   ├─ Charts                 // Chart containers
   ├─ Responsive             // Mobile styles
   └─ Utility classes        // Helpers
```

---

## 🔒 Security Considerations

### Implementate:

1. **SQLAlchemy ORM**: Prevenție SQL injection
2. **Secret Key**: Flask session security
3. **Input Validation**: API parameters
4. **Error Handling**: Try-catch blocks

### Recomandate pentru Producție:

1. **HTTPS**: SSL/TLS encryption
2. **CSRF Protection**: Flask-WTF
3. **Rate Limiting**: Flask-Limiter
4. **Authentication**: Flask-Login
5. **API Keys**: Environment variables (.env)

---

## 📊 Performance Optimizations

### Current:

1. **Database Indexing**: Pe symbol, score, sector
2. **Efficient Queries**: SQLAlchemy optimization
3. **Client Caching**: localStorage pentru preferences

### Possible Improvements:

1. **Redis Caching**: Cache API responses
2. **Database Sharding**: Pentru multe acțiuni
3. **CDN**: Serve static files
4. **Lazy Loading**: Load data incrementally
5. **Web Workers**: Background calculations

---

## 🧪 Testing Strategy

### Unit Tests (Recomandate):
```python
test_analyzer.py
   ├─ test_sentiment_score()
   ├─ test_technical_score()
   ├─ test_fundamental_score()
   ├─ test_target_price_calculation()
   └─ test_stop_loss_calculation()

test_data_fetcher.py
   ├─ test_demo_data_generation()
   ├─ test_api_calls()
   └─ test_error_handling()

test_models.py
   ├─ test_stock_creation()
   ├─ test_to_dict()
   └─ test_relationships()
```

### Integration Tests:
```python
test_api.py
   ├─ test_stocks_endpoint()
   ├─ test_stock_detail_endpoint()
   ├─ test_update_endpoint()
   └─ test_filtering()
```

---

## 🚀 Deployment Architecture

### Development:
```
Flask Built-in Server (port 5000)
SQLite Database (local file)
```

### Production:
```
Nginx (Reverse Proxy)
   ↓
Gunicorn (WSGI Server) × 4 workers
   ↓
Flask Application
   ↓
PostgreSQL/MySQL (Optional upgrade from SQLite)
```

### Scaling Strategy:
```
Load Balancer
   ├─ App Server 1
   ├─ App Server 2
   └─ App Server 3
       ↓
   Shared Database
       ↓
   Redis Cache
```

---

## 📈 Monitoring & Logging

### Logs:
```
Application Logs → stock_analyzer.log
   ├─ INFO: Update cycles
   ├─ WARNING: API failures
   └─ ERROR: Database errors

Access Logs → nginx/access.log
Error Logs → nginx/error.log
```

### Metrics (Recomandate):
- Request rate
- Response time
- Database query time
- Update success rate
- Stock count
- User activity

---

## 🔮 Future Enhancements

### Planned Features:
1. Machine Learning predictions
2. Multi-timeframe analysis
3. Portfolio tracking
4. Real-time websocket updates
5. Mobile app (React Native)
6. Export to Excel/PDF
7. Email/SMS alerts
8. Backtesting engine
9. Social trading features
10. API for third-party integrations

---

**Documentație tehnică completă pentru dezvoltatori 🛠️**
