# Ghid Vizual - Stock Market Analyzer Interface

## 📱 Dashboard Principal (`/`)

```
┌────────────────────────────────────────────────────────────────────────┐
│  🏠 Stock Analyzer Pro          Dashboard   Settings   [🔄 Refresh]   │
└────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  Bullish Stocks  │ │  Neutral Stocks  │ │  Bearish Stocks  │ │  Average Score   │
│       ↑          │ │       -          │ │       ↓          │ │       ⭐         │
│      12          │ │       5          │ │       3          │ │      65.3        │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  Filters & Search                                                       │
├────────────────────────────────────────────────────────────────────────┤
│  🔍 Search: [AAPL, MSFT...]                                            │
│                                                                         │
│  Sentiment: [All ▼]  Sector: [All Sectors ▼]  Min Score: [   ]       │
│  Sort By: [Total Score ▼]  Order: [↓]                                 │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  📊 Stock Analysis                    Last update: 5 minutes ago       │
├────────────────────────────────────────────────────────────────────────┤
│ Symbol│Company      │Sector│Price│Change│Target│Stop │Score│Sent│Tech│
├────────────────────────────────────────────────────────────────────────┤
│ AAPL  │Apple Inc.   │Tech  │175.5│ ↑2.3%│195.2 │162.3│ 78.5│ 72 │ 85 │
│       │             │      │     │      │      │     │🟢SB │    │    │
│       │             │      │     │      │      │     │ BUY │    │    │
├────────────────────────────────────────────────────────────────────────┤
│ MSFT  │Microsoft    │Tech  │410.2│ ↑1.8%│445.7 │385.5│ 75.2│ 70 │ 82 │
│       │             │      │     │      │      │     │🟢SB │    │    │
│       │             │      │     │      │      │     │ BUY │    │    │
├────────────────────────────────────────────────────────────────────────┤
│ TSLA  │Tesla Inc.   │Auto  │175.3│ ↓1.2%│188.5 │165.2│ 68.4│ 75 │ 65 │
│       │             │      │     │      │      │     │🔵B  │    │    │
│       │             │      │     │      │      │     │ BUY │    │    │
├────────────────────────────────────────────────────────────────────────┤
│ ...   │             │      │     │      │      │     │     │    │    │
└────────────────────────────────────────────────────────────────────────┘

      Next update: 4h 25m | Auto-updates: 6:30 AM EST & 10:30 AM EST
```

**Legendă Culori:**
- 🟢 Strong Bullish (75-100)
- 🔵 Bullish (60-75)
- ⚪ Neutral (40-60)
- 🟡 Bearish (25-40)
- 🔴 Strong Bearish (0-25)

---

## 📈 Detalii Acțiune (`/stock/AAPL`)

```
┌────────────────────────────────────────────────────────────────────────┐
│  🏠 Stock Analyzer Pro                            ← Back to Dashboard  │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  AAPL - Apple Inc.                                    $175.50          │
│  Technology                                            ↑ 2.35%          │
└────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  Total Score     │ │  Sentiment       │ │  Technical       │ │  Fundamental     │
│                  │ │                  │ │                  │ │                  │
│      78.5        │ │      72.0        │ │      85.0        │ │      76.0        │
│                  │ │                  │ │                  │ │                  │
│ 🟢 Strong Bullish│ │   35% weight     │ │   40% weight     │ │   25% weight     │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Current Price    │ │ 🎯 Target Price  │ │ 🛑 Stop Loss     │
│                  │ │                  │ │                  │
│    $175.50       │ │    $195.20       │ │    $162.30       │
│                  │ │                  │ │                  │
│                  │ │  Upside: +11.2%  │ │   Risk: -7.5%    │
└──────────────────┘ └──────────────────┘ └──────────────────┘

┌──────────────────────────────────┐ ┌──────────────────────────────────┐
│  📊 Price History (30 days)      │ │  📈 Score History (30 days)      │
│                                  │ │                                  │
│  180 ┤        ╭─╮                │ │  100┤                            │
│  178 ┤      ╭─╯ ╰╮               │ │   90┤        ╭─╮                 │
│  176 ┤    ╭─╯    ╰╮              │ │   80┤      ╭─╯ ╰─╮               │
│  174 ┤  ╭─╯       ╰╮             │ │   70┤    ╭─╯     ╰╮              │
│  172 ┤╭─╯          ╰─            │ │   60┤  ╭─╯        ╰─             │
│      └─────────────────────      │ │      └─────────────────────      │
│       1w    2w    3w    4w       │ │       1w    2w    3w    4w       │
└──────────────────────────────────┘ └──────────────────────────────────┘

┌──────────────────────────────────┐ ┌──────────────────────────────────┐
│  🔧 Technical Indicators         │ │  💰 Fundamental Metrics          │
│                                  │ │                                  │
│  RSI              45.32          │ │  P/E Ratio        28.50          │
│  MACD              0.1234        │ │  EPS              $6.15          │
│  SMA 50          $172.45         │ │  EPS Growth       12.3%          │
│  SMA 200         $168.90         │ │  Market Cap       $2.8T          │
│                                  │ │                                  │
└──────────────────────────────────┘ └──────────────────────────────────┘
```

---

## ⚙️ Settings Page (`/settings`)

```
┌────────────────────────────────────────────────────────────────────────┐
│  🏠 Stock Analyzer Pro          Dashboard   Settings                   │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  ⏰ Update Schedule                                                     │
├────────────────────────────────────────────────────────────────────────┤
│  Data este actualizată automat de 2 ori pe zi:                        │
│                                                                         │
│  • 6:30 AM EST - Pre-market update (3h înainte de NYSE open)          │
│  • 10:30 AM EST - Post-open update (1h după NYSE open)                │
│                                                                         │
│  NYSE Trading Hours: 9:30 AM - 4:00 PM EST                            │
│                                                                         │
│  [🔄 Trigger Manual Update]                                            │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  🧮 Scoring System                                                      │
├────────────────────────────────────────────────────────────────────────┤
│  Formula:                                                               │
│  Total Score = (Sentiment × 35%) + (Technical × 40%) + (Fundamental × 25%) │
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │
│  │ Sentiment (35%)  │  │ Technical (40%)  │  │ Fundamental (25%)│    │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤    │
│  │ • News: 40%     │  │ • RSI: 25%      │  │ • P/E: 30%      │    │
│  │ • Social: 30%   │  │ • MACD: 25%     │  │ • EPS: 25%      │    │
│  │ • Market: 30%   │  │ • MA: 30%       │  │ • Revenue: 25%  │    │
│  │                  │  │ • Volume: 20%   │  │ • Debt: 20%     │    │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘    │
│                                                                         │
│  Classification:                                                        │
│  75-100: 🟢 Strong Bullish → BUY                                       │
│  60-75:  🔵 Bullish → BUY                                              │
│  40-60:  ⚪ Neutral → HOLD                                             │
│  25-40:  🟡 Bearish → SELL                                             │
│  0-25:   🔴 Strong Bearish → SELL                                      │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  💵 Price Target & Stop Loss                                           │
├────────────────────────────────────────────────────────────────────────┤
│  Target Price Formula:                                                  │
│  Target = Current Price × (1 + Expected Return)                        │
│  Expected Return = (Technical + Fundamental) / 200 × Risk Multiplier   │
│                                                                         │
│  Stop Loss Formula:                                                     │
│  Stop Loss = Current Price × (1 - Risk Factor)                         │
│  Risk Factor = (100 - Total Score) / 100 × 0.15                        │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  📊 System Information                                                  │
├────────────────────────────────────────────────────────────────────────┤
│  Database:            SQLite (Local)                                   │
│  Backend:             Python Flask                                      │
│  Frontend:            Bootstrap 5, JavaScript, Chart.js                │
│  Data Mode:           Simulated Data (Demo)                            │
│  Total Stocks Tracked: 20                                              │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│  📜 Recent Updates                                                      │
├────────────────────────────────────────────────────────────────────────┤
│  manual                                    2024-03-25 14:30:15         │
│  ✅ success                                Stocks updated: 20           │
│  ────────────────────────────────────────────────────────────────────  │
│  post_open                                 2024-03-25 10:30:00         │
│  ✅ success                                Stocks updated: 20           │
│  ────────────────────────────────────────────────────────────────────  │
│  pre_market                                2024-03-25 06:30:00         │
│  ✅ success                                Stocks updated: 20           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📱 Mobile View (Responsive)

```
┌──────────────────────┐
│ ☰ Stock Analyzer Pro │
└──────────────────────┘

┌──────────────────────┐
│  Bullish Stocks      │
│       ↑              │
│      12              │
└──────────────────────┘

┌──────────────────────┐
│  Neutral Stocks      │
│       -              │
│       5              │
└──────────────────────┘

┌──────────────────────┐
│  Average Score       │
│       ⭐             │
│      65.3            │
└──────────────────────┘

┌──────────────────────┐
│  🔍 Search Symbol    │
│  [             ]     │
│                      │
│  Sentiment: [All ▼] │
│  Sector: [All ▼]    │
│  Min Score: [   ]   │
│  Sort: [Score ▼]    │
└──────────────────────┘

┌──────────────────────┐
│  📊 Stocks           │
├──────────────────────┤
│ AAPL                 │
│ Apple Inc.           │
│ $175.50  ↑ 2.3%     │
│ Score: 78.5 🟢      │
│ Target: $195.20      │
│ [View Details]       │
├──────────────────────┤
│ MSFT                 │
│ Microsoft Corp.      │
│ $410.20  ↑ 1.8%     │
│ Score: 75.2 🟢      │
│ Target: $445.70      │
│ [View Details]       │
├──────────────────────┤
│ ...                  │
└──────────────────────┘
```

---

## 🎨 Color Scheme

### Score Indicators:
```
┌─────────────────────────────────────┐
│  Score Range    Color      Badge    │
├─────────────────────────────────────┤
│  75-100         🟢 Green   SB       │
│  60-75          🔵 Blue    B        │
│  40-60          ⚪ Gray    N        │
│  25-40          🟡 Yellow  Be       │
│  0-25           🔴 Red     SBe      │
└─────────────────────────────────────┘

SB  = Strong Bullish
B   = Bullish
N   = Neutral
Be  = Bearish
SBe = Strong Bearish
```

### Price Changes:
```
┌─────────────────────────────────────┐
│  Change         Color      Icon     │
├─────────────────────────────────────┤
│  Positive       🟢 Green   ↑        │
│  Negative       🔴 Red     ↓        │
│  No change      ⚪ Gray    -        │
└─────────────────────────────────────┘
```

---

## 🔄 Interactive Elements

### Dashboard Filters:
```
[Search Box] ──→ Real-time filter by symbol/name
[Sentiment]  ──→ Filter by classification
[Sector]     ──→ Filter by industry sector
[Min Score]  ──→ Filter by minimum score
[Sort By]    ──→ Sort column selection
[Order]      ──→ Ascending/Descending
[Refresh]    ──→ Reload all data
```

### Stock Detail Page:
```
[Back Button]     ──→ Return to dashboard
[Charts]          ──→ Interactive hover tooltips
[View Details]    ──→ Navigate to individual stock
```

### Settings Page:
```
[Manual Update]   ──→ Trigger immediate data refresh
[Update Log]      ──→ View update history
```

---

## 📊 Chart Types

### Price History Chart:
```
Line chart showing:
- X-axis: Time (30 days)
- Y-axis: Price ($)
- Tooltip: Date, exact price
- Color: Teal/Blue
```

### Score History Chart:
```
Line chart showing:
- X-axis: Time (30 days)
- Y-axis: Score (0-100)
- Tooltip: Date, exact score
- Color: Purple
```

---

## 🎯 User Journey Examples

### Finding Bullish Opportunities:
```
1. Dashboard → Set "Sentiment: Bullish"
2. Set "Min Score: 70"
3. Sort by "Total Score ↓"
4. Review top results
5. Click symbol → View details
6. Check charts + metrics
7. Make investment decision
```

### Tracking Specific Stock:
```
1. Dashboard → Search "AAPL"
2. Click AAPL symbol
3. Review detailed analysis
4. Check price charts
5. Compare target vs current
6. Monitor stop loss level
```

### System Configuration:
```
1. Click "Settings"
2. Review scoring formula
3. Check update schedule
4. Trigger manual update if needed
5. Review recent update logs
```

---

**Ghid vizual complet pentru navigarea aplicației! 🎨📱**
