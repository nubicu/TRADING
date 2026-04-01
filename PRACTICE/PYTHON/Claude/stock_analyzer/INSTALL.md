# Ghid de Instalare - Stock Market Analyzer

## Cerințe de Sistem

### Software Necesar
- **Python**: 3.8 sau mai nou
- **pip**: Package manager pentru Python
- **Browser modern**: Chrome, Firefox, Safari, Edge

### Sistem de Operare
- Linux (recomandat)
- macOS
- Windows (WSL recomandat)

## Instalare Pas cu Pas

### 1. Descărcare Proiect
```bash
cd /path/to/your/directory
# Dacă aveți proiectul, navigați în directorul stock_analyzer
cd stock_analyzer
```

### 2. Instalare Dependințe Python

#### Metoda 1: Cu Virtual Environment (Recomandat)
```bash
# Creează virtual environment
python3 -m venv venv

# Activează environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalează dependințe
pip install -r requirements.txt
```

#### Metoda 2: Direct (Nu recomandat)
```bash
pip install -r requirements.txt
```

### 3. Configurare API Keys (Opțional)

Pentru date real-time, puteți configura API keys:

```bash
# Copiați template-ul
cp .env.example .env

# Editați .env și adăugați keys
nano .env
```

**API Keys disponibile gratuit:**
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key
  - Limită: 5 requests/min, 500/zi (gratuit)
- **News API**: https://newsapi.org/register
  - Limită: 100 requests/zi (gratuit)

**IMPORTANT**: Aplicația funcționează perfect și **fără API keys**, folosind date simulate.

## Pornire Aplicație

### Metoda 1: Script Automat
```bash
chmod +x start.sh
./start.sh
```

### Metoda 2: Manual

#### Terminal 1 - Flask Server
```bash
source venv/bin/activate
python app.py
```

Serverul va porni la: **http://localhost:5000**

#### Terminal 2 - Scheduler (Opțional, pentru update-uri automate)
```bash
source venv/bin/activate
python scheduler.py
```

## Verificare Instalare

### 1. Verifică Server
Deschide browser la: **http://localhost:5000**

Ar trebui să vezi dashboard-ul principal.

### 2. Verifică Baza de Date
```bash
# În terminal Python
python3
>>> from app import app, db, Stock
>>> with app.app_context():
...     print(f"Total stocks: {Stock.query.count()}")
>>> exit()
```

### 3. Test Update Manual
În browser:
1. Mergi la **Settings** (`http://localhost:5000/settings`)
2. Click pe **"Trigger Manual Update"**
3. Verifică că datele se încarcă

## Structura Proiectului După Instalare

```
stock_analyzer/
├── database.db          # Bază de date SQLite (creată automat)
├── venv/               # Virtual environment (dacă folosești)
├── app.py              # Server Flask ✓
├── scheduler.py        # Scheduler pentru update-uri ✓
├── models.py           # Modele DB ✓
├── analyzer.py         # Logică scoring ✓
├── data_fetcher.py     # Fetch date ✓
├── requirements.txt    # Dependințe ✓
├── .env               # Config (opțional)
├── templates/         # HTML templates ✓
│   ├── index.html
│   ├── stock_detail.html
│   └── settings.html
└── static/            # CSS + JS ✓
    ├── css/style.css
    └── js/main.js
```

## Troubleshooting

### Problema: ModuleNotFoundError
**Soluție**: Instalează din nou dependințele
```bash
pip install -r requirements.txt
```

### Problema: Port 5000 ocupat
**Soluție**: Schimbă portul în `app.py` (ultima linie):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Port 5001
```

### Problema: Database locked
**Soluție**: Închide toate conexiunile și șterge database.db
```bash
rm database.db
python app.py  # Va recrea baza de date
```

### Problema: Scheduler nu pornește
**Soluție**: Verifică că Flask server rulează
```bash
# Verifică dacă serverul răspunde
curl http://localhost:5000/api/stocks
```

### Problema: No data displayed
**Soluție**: Trigger manual update
1. Du-te la Settings
2. Click "Trigger Manual Update"
3. Așteaptă 30-60 secunde

## Configurare pentru Producție

### 1. Dezactivează Debug Mode
În `app.py`, schimbă:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### 2. Folosește Gunicorn (Production Server)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Configurare Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/stock_analyzer/static;
    }
}
```

### 4. Configurare Systemd (Auto-start)

#### Flask Service
```ini
# /etc/systemd/system/stock-analyzer.service
[Unit]
Description=Stock Market Analyzer - Flask App
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/stock_analyzer
Environment="PATH=/path/to/stock_analyzer/venv/bin"
ExecStart=/path/to/stock_analyzer/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Scheduler Service
```ini
# /etc/systemd/system/stock-scheduler.service
[Unit]
Description=Stock Market Analyzer - Scheduler
After=network.target stock-analyzer.service

[Service]
User=your-user
WorkingDirectory=/path/to/stock_analyzer
Environment="PATH=/path/to/stock_analyzer/venv/bin"
ExecStart=/path/to/stock_analyzer/venv/bin/python scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Enable Services
```bash
sudo systemctl daemon-reload
sudo systemctl enable stock-analyzer
sudo systemctl enable stock-scheduler
sudo systemctl start stock-analyzer
sudo systemctl start stock-scheduler
```

## Performance Tips

### 1. Database Optimization
```bash
# Periodic vacuum
sqlite3 database.db "VACUUM;"
```

### 2. Logging
Adaugă logging în `app.py`:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 3. Caching (Redis - opțional)
```bash
pip install flask-caching redis
```

## Backup și Restore

### Backup Database
```bash
# Backup simplu
cp database.db database.db.backup

# Backup cu timestamp
cp database.db "database.db.$(date +%Y%m%d_%H%M%S)"
```

### Restore Database
```bash
cp database.db.backup database.db
```

## Update Aplicație

```bash
# Oprește serviciile
sudo systemctl stop stock-analyzer stock-scheduler

# Update cod
git pull  # sau copiază fișierele noi

# Update dependințe
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart servicii
sudo systemctl start stock-analyzer stock-scheduler
```

## Support și Documentație

- **README.md**: Overview general
- **INSTALL.md**: Acest fișier
- **API Documentation**: Vezi comentariile în `app.py`

## Licență
MIT License - Vezi README.md pentru detalii
