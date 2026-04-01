"""
Data Fetcher - Obține date financiare de pe API-uri
Pentru demo, folosește date simulate dacă API keys nu sunt disponibile
"""
import os
import random
import re
import requests
import time
from datetime import datetime, timedelta
from textblob import TextBlob
from bs4 import BeautifulSoup

try:
    import yfinance as yf
except ImportError:
    yf = None
from stock_lists import get_all_stocks

class DataFetcher:
    """Fetcher pentru date financiare și sentiment"""
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.use_yahoo_data = True
        self.use_demo_sentiment = not bool(self.news_api_key)
        self.rate_limit_delay = 0.25  # 250ms between requests
        self.last_request_time = 0
        self.yahoo_rate_limited = False  # Track if we're hitting rate limits
        self.rate_limit_reset_time = None

        if self.use_demo_sentiment:
            print("⚠️  News API key not found - using simulated sentiment data")

        print(f"📊 Loaded {len(get_all_stocks())} stocks from NYSE and NASDAQ")
    
    def get_stock_list(self):
        """Returnează lista completă de acțiuni NYSE + NASDAQ"""
        return get_all_stocks()
    
    def _apply_rate_limit(self):
        """Apply rate limiting to avoid 429 errors"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    def _is_rate_limited(self):
        """Check if we should skip Yahoo API and go straight to yfinance"""
        if self.rate_limit_reset_time and time.time() < self.rate_limit_reset_time:
            return True
        return self.yahoo_rate_limited
    
    def _handle_rate_limit(self):
        """Mark that we're rate limited and set reset time"""
        self.yahoo_rate_limited = True
        self.rate_limit_reset_time = time.time() + 60  # Wait 60 seconds before retrying
        print("⚠️  Yahoo Finance rate limit detected. Switching to yfinance fallback for next 60s")
    
    def _reset_rate_limit(self):
        """Reset rate limit flag"""
        if time.time() > (self.rate_limit_reset_time or 0):
            self.yahoo_rate_limited = False
            self.rate_limit_reset_time = None
    
    def _compute_sma(self, prices, period):
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period

    def _compute_rsi(self, prices, period=14):
        if len(prices) < period + 1:
            return None

        closes = prices[-(period + 1):]
        gains = 0.0
        losses = 0.0

        for i in range(1, len(closes)):
            delta = closes[i] - closes[i - 1]
            if delta > 0:
                gains += delta
            else:
                losses += abs(delta)

        avg_gain = gains / period
        avg_loss = losses / period

        if avg_loss == 0:
            return 100.0 if avg_gain > 0 else 50.0

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def _compute_ema(self, prices, period):
        if len(prices) < period:
            return None

        k = 2 / (period + 1)
        ema_values = []
        sma = sum(prices[:period]) / period
        ema_values.append(sma)

        for price in prices[period:]:
            ema = (price - ema_values[-1]) * k + ema_values[-1]
            ema_values.append(ema)

        return ema_values

    def _compute_macd(self, prices):
        if len(prices) < 26:
            return None, None

        ema12 = self._compute_ema(prices, 12)
        ema26 = self._compute_ema(prices, 26)

        if not ema12 or not ema26:
            return None, None

        # align ema12 with ema26 by using the tail of ema12
        ema12_aligned = ema12[len(ema12) - len(ema26):]
        macd_series = [ema12_aligned[i] - ema26[i] for i in range(len(ema26))]

        if len(macd_series) < 9:
            return macd_series[-1], None if macd_series else None

        signal = self._compute_ema(macd_series, 9)
        return round(macd_series[-1], 4), round(signal[-1], 4) if signal else None

    def _fetch_price_from_summary(self, symbol):
        """Fallback to Yahoo quoteSummary price module"""
        try:
            url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}'
            params = {'modules': 'price'}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            result = data.get('quoteSummary', {}).get('result', [])

            if not result:
                return None

            price_info = result[0].get('price', {})
            current_price = price_info.get('regularMarketPrice', {}).get('raw')
            previous_close = price_info.get('regularMarketPreviousClose', {}).get('raw')
            volume = price_info.get('regularMarketVolume', {}).get('raw')

            if current_price is None and previous_close is None and volume is None:
                return None

            return {
                'current_price': current_price,
                'previous_close': previous_close,
                'volume': volume
            }
        except Exception as e:
            print(f"Warning: Could not fetch fallback price for {symbol} from quoteSummary: {e}")
            return None

    def _fetch_price_from_chart(self, symbol):
        """Fallback to Yahoo chart endpoint for latest close price"""
        try:
            now = int(datetime.utcnow().timestamp())
            period1 = now - 3 * 24 * 3600
            url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
            params = {
                'interval': '1d',
                'period1': period1,
                'period2': now,
                'includePrePost': 'false',
                'events': 'div,splits'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            result = data.get('chart', {}).get('result', [])
            if not result:
                return None
            quote = result[0].get('indicators', {}).get('quote', [{}])[0]
            closes = [c for c in quote.get('close', []) if c is not None]
            volumes = [v for v in quote.get('volume', []) if v is not None]
            if not closes:
                return None
            current_price = closes[-1]
            previous_close = closes[-2] if len(closes) >= 2 else None
            volume = volumes[-1] if volumes else None
            return {
                'current_price': current_price,
                'previous_close': previous_close,
                'volume': volume
            }
        except Exception as e:
            print(f"Warning: Could not fetch fallback price for {symbol} from chart: {e}")
            return None

    def _fetch_price_from_yfinance(self, symbol):
        """Fallback to yfinance package if installed"""
        if yf is None:
            return None

        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='2d')
            if hist.empty:
                return None

            current_price = float(hist['Close'].iloc[-1])
            previous_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else None
            volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else None

            return {
                'current_price': current_price,
                'previous_close': previous_close,
                'volume': volume
            }
        except Exception as e:
            print(f"Warning: Could not fetch fallback price for {symbol} from yfinance: {e}")
            return None

    def _fetch_technical_from_yfinance(self, symbol):
        """Fallback technical indicators from yfinance if chart API fails"""
        if yf is None:
            return None

        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1y')
            if hist.empty or len(hist) < 50:
                return None

            closes = hist['Close'].dropna().tolist()
            volumes = hist['Volume'].dropna().tolist()

            sma_50 = self._compute_sma(closes, 50)
            sma_200 = self._compute_sma(closes, 200)
            macd_val, macd_signal_val = self._compute_macd(closes)

            avg_volume = sum(volumes[-20:]) / len(volumes[-20:]) if len(volumes) >= 20 else (sum(volumes) / len(volumes) if volumes else 50000000)

            return {
                'rsi': round(self._compute_rsi(closes) or 50, 2),
                'macd': macd_val if macd_val is not None else 0.0,
                'macd_signal': macd_signal_val if macd_signal_val is not None else 0.0,
                'sma_50': round(sma_50, 2) if sma_50 else None,
                'sma_200': round(sma_200, 2) if sma_200 else None,
                'avg_volume': int(avg_volume) if avg_volume else 50000000,
            }

        except Exception as e:
            print(f"Warning: Could not fetch technical indicators for {symbol} from yfinance: {e}")
            return None

    def _fetch_price_from_google_finance(self, symbol):
        """Fallback to Google Finance via webscraping"""
        try:
            from bs4 import BeautifulSoup
            
            # Try to get price from Google Finance
            url = f'https://www.google.com/finance/quote/{symbol}:NYSE'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for price in various possible locations
            price_elements = soup.find_all(class_=re.compile(r'[Pp]rice|[Vv]alue'))
            
            for elem in price_elements:
                price_text = elem.get_text(strip=True)
                # Extract numeric value
                price_match = re.search(r'(\d+(?:\.\d{2})?)', price_text)
                if price_match:
                    try:
                        current_price = float(price_match.group(1))
                        return {
                            'current_price': current_price,
                            'previous_close': None,
                            'volume': None
                        }
                    except:
                        pass
            
            return None
        except Exception as e:
            print(f"Warning: Could not fetch price for {symbol} from Google Finance: {e}")
            return None

    def _fetch_price_from_finnhub(self, symbol):
        """Fallback to Finnhub free API (1 request/sec limit)"""
        try:
            # Finnhub offers a free tier with data (requires registration but free)
            # Public endpoint for quote data
            url = f'https://finnhub.io/api/v1/quote'
            params = {
                'symbol': symbol,
                'token': 'demo'  # 'demo' token has limited requests but works
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current_price = data.get('c')  # current price
                previous_close = data.get('pc')  # previous close
                volume = data.get('v')  # volume (not always available)
                
                if current_price is not None or previous_close is not None:
                    return {
                        'current_price': current_price,
                        'previous_close': previous_close,
                        'volume': volume
                    }
            
            return None
        except Exception as e:
            print(f"Warning: Could not fetch price for {symbol} from Finnhub: {e}")
            return None

    def _fetch_price_from_alphavantage(self, symbol):
        """Fallback to Alpha Vantage if API key is available"""
        if not self.alpha_vantage_key:
            return None
        
        try:
            url = 'https://www.alphavantage.co/query'
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            quote = data.get('Global Quote', {})
            
            if quote:
                current_price = quote.get('05. price')
                previous_close = quote.get('08. previous close')
                volume = quote.get('06. volume')
                
                return {
                    'current_price': float(current_price) if current_price and current_price != 'N/A' else None,
                    'previous_close': float(previous_close) if previous_close and previous_close != 'N/A' else None,
                    'volume': int(volume) if volume and volume != 'N/A' else None
                }
            
            return None
        except Exception as e:
            print(f"Warning: Could not fetch price for {symbol} from Alpha Vantage: {e}")
            return None

    def fetch_price_data(self, symbol):
        """Obține date despre preț (Yahoo Finance în mod implicit, cu fallback-uri multiple)"""
        if not self.use_yahoo_data:
            return self._generate_demo_price_data(symbol)

        # If we're rate limited globally, skip straight to alternatives
        if self._is_rate_limited():
            print(f"⏭️  Skipping Yahoo API for {symbol} (rate limited) - trying alternatives")
            # Try multiple fallbacks in order
            fallback_sources = [
                (self._fetch_price_from_alphavantage, "Alpha Vantage"),
                (self._fetch_price_from_finnhub, "Finnhub"),
                (self._fetch_price_from_yfinance, "yfinance"),
                (self._fetch_price_from_google_finance, "Google Finance"),
            ]
            
            for fetch_func, source_name in fallback_sources:
                result = fetch_func(symbol)
                if result and result.get('current_price') is not None:
                    print(f"✅ Got price for {symbol} from {source_name}")
                    return result
            
            return {'current_price': None, 'previous_close': None, 'volume': None}

        try:
            self._apply_rate_limit()  # Enforce delay before request
            
            url = 'https://query1.finance.yahoo.com/v7/finance/quote'
            params = {'symbols': symbol}
            response = requests.get(url, params=params, timeout=10)
            
            # Check for rate limiting
            if response.status_code == 429:
                self._handle_rate_limit()
                print(f"Error fetching price for {symbol}: {response.status_code} - rate limited")
                # Try alternatives
                fallback_sources = [
                    (self._fetch_price_from_alphavantage, "Alpha Vantage"),
                    (self._fetch_price_from_finnhub, "Finnhub"),
                    (self._fetch_price_from_yfinance, "yfinance"),
                    (self._fetch_price_from_google_finance, "Google Finance"),
                ]
                
                for fetch_func, source_name in fallback_sources:
                    result = fetch_func(symbol)
                    if result and result.get('current_price') is not None:
                        print(f"✅ Got price for {symbol} from {source_name}")
                        return result
                
                return {'current_price': None, 'previous_close': None, 'volume': None}
            
            response.raise_for_status()
            data = response.json()
            quote = data.get('quoteResponse', {}).get('result', [])

            if quote:
                quote = quote[0]
                current_price = quote.get('regularMarketPrice')
                previous_close = quote.get('regularMarketPreviousClose')
                volume = quote.get('regularMarketVolume')

                if current_price is not None or previous_close is not None or volume is not None:
                    return {
                        'current_price': current_price,
                        'previous_close': previous_close,
                        'volume': volume
                    }

            # Try multiple fallbacks in order if quote endpoint lacks data
            fallback_sources = [
                (self._fetch_price_from_alphavantage, "Alpha Vantage"),
                (self._fetch_price_from_finnhub, "Finnhub"),
                (self._fetch_price_from_summary, "Yahoo quoteSummary"),
                (self._fetch_price_from_chart, "Yahoo chart"),
                (self._fetch_price_from_yfinance, "yfinance"),
                (self._fetch_price_from_google_finance, "Google Finance"),
            ]
            
            for fetch_func, source_name in fallback_sources:
                result = fetch_func(symbol)
                if result and result.get('current_price') is not None:
                    print(f"✅ Got price for {symbol} from {source_name}")
                    return result

            print(f"Warning: No price data found for {symbol} from any source")
            return {'current_price': None, 'previous_close': None, 'volume': None}

        except requests.exceptions.RequestException as e:
            error_str = str(e)
            if '429' in error_str or 'Too Many Requests' in error_str:
                self._handle_rate_limit()
            
            print(f"Error fetching price for Yahoo API for {symbol}: {e}")
            
            # Try fallbacks in order
            fallback_sources = [
                (self._fetch_price_from_alphavantage, "Alpha Vantage"),
                (self._fetch_price_from_finnhub, "Finnhub"),
                (self._fetch_price_from_summary, "Yahoo quoteSummary"),
                (self._fetch_price_from_chart, "Yahoo chart"),
                (self._fetch_price_from_yfinance, "yfinance"),
                (self._fetch_price_from_google_finance, "Google Finance"),
            ]
            
            for fetch_func, source_name in fallback_sources:
                result = fetch_func(symbol)
                if result and result.get('current_price') is not None:
                    print(f"✅ Got price for {symbol} from {source_name}")
                    return result
            
            return {'current_price': None, 'previous_close': None, 'volume': None}
    
    def fetch_technical_indicators(self, symbol):
        """Obține indicatori tehnici din Yahoo Finance chart (1d)"""
        if not self.use_yahoo_data:
            return self._generate_demo_technical_data(symbol)

        try:
            now = int(datetime.utcnow().timestamp())
            period1 = now - 365 * 24 * 3600  # 1 an
            url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
            params = {
                'symbol': symbol,
                'interval': '1d',
                'period1': period1,
                'period2': now,
                'includePrePost': 'false',
                'events': 'div,splits'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            result = data.get('chart', {}).get('result', [])

            if not result:
                raise ValueError(f'No chart data for {symbol}')

            indicators = result[0].get('indicators', {}).get('quote', [{}])[0]
            closes = indicators.get('close', [])
            volumes = indicators.get('volume', [])
            closes = [c for c in closes if c is not None]
            volumes = [v for v in volumes if v is not None]

            # Calculate SMA with real data
            sma_50 = self._compute_sma(closes, 50)
            sma_200 = self._compute_sma(closes, 200)

            macd_val, macd_signal_val = self._compute_macd(closes)

            # Calculate average volume
            avg_volume = sum(volumes[-20:]) / len(volumes[-20:]) if len(volumes) >= 20 else (sum(volumes) / len(volumes) if volumes else 50000000)

            return {
                'rsi': round(self._compute_rsi(closes) or 50, 2),
                'macd': macd_val if macd_val is not None else 0.0,
                'macd_signal': macd_signal_val if macd_signal_val is not None else 0.0,
                'sma_50': round(sma_50, 2) if sma_50 else None,
                'sma_200': round(sma_200, 2) if sma_200 else None,
                'avg_volume': int(avg_volume) if avg_volume else 50000000,
            }

        except Exception as e:
            print(f"Error fetching technical indicators for {symbol}: {e}")

        # Try yfinance fallback then demo
        yfinance_tech = self._fetch_technical_from_yfinance(symbol)
        if yfinance_tech:
            return yfinance_tech

        return self._generate_demo_technical_data(symbol)
    
    def fetch_fundamental_data(self, symbol):
        """Obține date fundamentale din Yahoo Finance quoteSummary"""
        if not self.use_yahoo_data:
            return self._generate_demo_fundamental_data(symbol)

        try:
            url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}'
            params = {'modules': 'summaryDetail,defaultKeyStatistics,financialData,earningsHistory'}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            result = data.get('quoteSummary', {}).get('result', [])

            if not result:
                raise ValueError(f'No summary for {symbol}')

            summary = result[0]
            summary_detail = summary.get('summaryDetail', {})
            statistics = summary.get('defaultKeyStatistics', {})
            financial = summary.get('financialData', {})
            earnings = summary.get('earningsHistory', {})

            pe_ratio = summary_detail.get('trailingPE', {}).get('raw')
            eps = statistics.get('trailingEps', {}).get('raw')
            
            # Try multiple sources for EPS Growth
            eps_growth = None
            if financial.get('earningsGrowth'):
                eps_growth = financial.get('earningsGrowth', {}).get('raw')
            elif financial.get('earnings'):
                # Calculate from earnings data
                earnings_val = financial.get('earnings', {})
                if isinstance(earnings_val, dict) and earnings_val.get('raw'):
                    eps_growth = (earnings_val['raw'] - eps) / eps * 100 if eps and eps != 0 else None
            else:
                # Try from earnings history
                history = earnings.get('history', [])
                if len(history) >= 2:
                    recent = history[0].get('epsActual', {}).get('raw')
                    previous = history[1].get('epsActual', {}).get('raw')
                    if recent and previous and previous != 0:
                        eps_growth = ((recent - previous) / previous) * 100
            
            revenue_growth = financial.get('revenueGrowth', {}).get('raw')
            debt_to_equity = statistics.get('debtToEquity', {}).get('raw') or financial.get('debtToEquity', {}).get('raw')
            market_cap = summary_detail.get('marketCap', {}).get('raw')

            return {
                'pe_ratio': float(pe_ratio) if pe_ratio is not None else None,
                'eps': float(eps) if eps is not None else None,
                'eps_growth': float(eps_growth * 100) if eps_growth is not None and isinstance(eps_growth, float) else eps_growth if eps_growth is not None else None,
                'revenue_growth': float(revenue_growth * 100) if revenue_growth is not None else None,
                'debt_to_equity': float(debt_to_equity) if debt_to_equity is not None else None,
                'market_cap': int(market_cap) if market_cap is not None else None,
            }

        except Exception as e:
            print(f"Error fetching fundamental data for {symbol}: {e}")
            return self._generate_demo_fundamental_data(symbol)
    
    def _fetch_stocktwits_sentiment(self, symbol):
        """Obține sentiment din StockTwits (API public, fără cheie necesară)"""
        try:
            url = f'https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'messages' in data and data['messages']:
                sentiments = []
                for message in data['messages'][:30]:
                    sentiment = message.get('entities', {}).get('sentiment')
                    if sentiment:
                        # StockTwits: Bullish = positive, Bearish = negative
                        if sentiment.get('basic') == 'Bullish':
                            sentiments.append(0.7)
                        elif sentiment.get('basic') == 'Bearish':
                            sentiments.append(-0.7)
                
                if sentiments:
                    return sum(sentiments) / len(sentiments)
            
            return random.uniform(-0.3, 0.5)
        except Exception as e:
            print(f"Warning: Could not fetch StockTwits sentiment for {symbol}: {e}")
            return random.uniform(-0.3, 0.5)
    
    def _calculate_market_correlation(self, symbol):
        """Calculează corelația dintre stock și S&P 500"""
        try:
            now = int(datetime.utcnow().timestamp())
            period1 = now - 90 * 24 * 3600  # 3 luni de date
            
            # Fetch stock prices
            url_stock = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
            params = {
                'interval': '1d',
                'period1': period1,
                'period2': now
            }
            response_stock = requests.get(url_stock, params=params, timeout=10)
            response_stock.raise_for_status()
            data_stock = response_stock.json()
            
            # Fetch S&P 500 prices
            url_sp500 = f'https://query1.finance.yahoo.com/v8/finance/chart/^GSPC'
            response_sp500 = requests.get(url_sp500, params=params, timeout=10)
            response_sp500.raise_for_status()
            data_sp500 = response_sp500.json()
            
            # Extract prices
            stock_closes = data_stock.get('chart', {}).get('result', [{}])[0].get('indicators', {}).get('quote', [{}])[0].get('close', [])
            sp500_closes = data_sp500.get('chart', {}).get('result', [{}])[0].get('indicators', {}).get('quote', [{}])[0].get('close', [])
            
            stock_closes = [p for p in stock_closes if p is not None]
            sp500_closes = [p for p in sp500_closes if p is not None]
            
            if len(stock_closes) < 10 or len(sp500_closes) < 10:
                return random.uniform(-0.3, 0.9)
            
            # Align lengths
            min_len = min(len(stock_closes), len(sp500_closes))
            stock_closes = stock_closes[-min_len:]
            sp500_closes = sp500_closes[-min_len:]
            
            # Calculate returns
            stock_returns = [(stock_closes[i] - stock_closes[i-1]) / stock_closes[i-1] if stock_closes[i-1] != 0 else 0 
                           for i in range(1, len(stock_closes))]
            sp500_returns = [(sp500_closes[i] - sp500_closes[i-1]) / sp500_closes[i-1] if sp500_closes[i-1] != 0 else 0 
                           for i in range(1, len(sp500_closes))]
            
            # Calculate correlation
            if len(stock_returns) < 5 or len(sp500_returns) < 5:
                return random.uniform(-0.3, 0.9)
            
            mean_stock = sum(stock_returns) / len(stock_returns)
            mean_sp500 = sum(sp500_returns) / len(sp500_returns)
            
            numerator = sum((stock_returns[i] - mean_stock) * (sp500_returns[i] - mean_sp500) 
                          for i in range(len(stock_returns)))
            
            std_stock = (sum((r - mean_stock) ** 2 for r in stock_returns) / len(stock_returns)) ** 0.5
            std_sp500 = (sum((r - mean_sp500) ** 2 for r in sp500_returns) / len(sp500_returns)) ** 0.5
            
            if std_stock == 0 or std_sp500 == 0:
                return 0.5
            
            correlation = numerator / (len(stock_returns) * std_stock * std_sp500)
            return max(-1, min(1, correlation))
        
        except Exception as e:
            print(f"Warning: Could not calculate market correlation for {symbol}: {e}")
            return random.uniform(-0.3, 0.9)

    def _fetch_yahoo_news(self, symbol, company_name):
        """Obține articole de știri de la Yahoo Finance ca fallback"""
        def parse_news_data(data):
            raw_news = data.get('news') or data.get('items') or []
            if not raw_news:
                return None

            articles = []
            sentiments = []

            for item in raw_news[:5]:
                title = item.get('title') or item.get('headline') or ''
                description = item.get('summary') or item.get('snippet') or item.get('abstract') or ''
                url_article = item.get('link') or item.get('url') or ''
                source = item.get('publisher') or item.get('source') or ''
                published_at = ''

                if item.get('providerPublishTime'):
                    try:
                        published_at = datetime.fromtimestamp(item.get('providerPublishTime')).isoformat()
                    except Exception:
                        published_at = ''
                elif item.get('published'):
                    published_at = item.get('published')

                text = f"{title} {description}"
                polarity = TextBlob(text).sentiment.polarity
                sentiments.append(polarity)

                articles.append({
                    'title': title,
                    'description': description,
                    'url': url_article,
                    'source': source,
                    'published_at': published_at,
                    'sentiment': polarity
                })

            return {'articles': articles, 'sentiments': sentiments}

        for query in (company_name, symbol):
            try:
                url = 'https://query1.finance.yahoo.com/v1/finance/search'
                params = {'q': query, 'newsCount': 10, 'quotesCount': 0}
                response = requests.get(url, params=params, timeout=10)

                if response.status_code != 200:
                    print(f"Warning: Yahoo news call for {query} returned {response.status_code}")
                    continue

                data = response.json()
                parsed = parse_news_data(data)
                if parsed and parsed['articles']:
                    print(f"DEBUG: Yahoo news found {len(parsed['articles'])} articles for query '{query}'")
                    return parsed

            except Exception as e:
                print(f"Warning: Could not fetch Yahoo news for {symbol} with query '{query}': {e}")
                continue

        print(f"Warning: No Yahoo news found for {symbol} ({company_name})")
        return None

    def _fetch_google_news(self, symbol, company_name):
        """Obține articole de știri de pe Google News ca fallback"""
        try:
            query = f"{symbol} stock"
            url = 'https://news.google.com/search'
            params = {
                'q': query,
                'hl': 'en-US',
                'gl': 'US',
                'ceid': 'US:en'
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            html = response.text
            matches = re.findall(r'<a[^>]+href="(/articles/[^"]+)"[^>]*>(.*?)<\/a>', html, re.S)
            articles = []
            sentiments = []

            for href, title_html in matches:
                title = re.sub('<[^<]+?>', '', title_html).strip()
                if not title:
                    continue

                article_url = href
                if article_url.startswith('/articles/'):
                    article_url = 'https://news.google.com' + article_url

                polarity = TextBlob(title).sentiment.polarity
                sentiments.append(polarity)
                articles.append({
                    'title': title,
                    'description': '',
                    'url': article_url,
                    'source': 'Google News',
                    'published_at': '',
                    'sentiment': polarity
                })

                if len(articles) >= 5:
                    break

            if articles:
                print(f"DEBUG: Google News found {len(articles)} articles for {symbol}")
                return {'articles': articles, 'sentiments': sentiments}

        except Exception as e:
            print(f"Warning: Could not fetch Google news for {symbol}: {e}")

        print(f"Warning: No Google news found for {symbol} ({company_name})")
        return None

    def _fetch_alternative_news(self, symbol, company_name):
        """Obține știri din surse alternative gratuite"""
        # Try RSS feeds from financial news sources first (more reliable)
        rss_result = self._fetch_rss_news(symbol, company_name)
        if rss_result and rss_result.get('articles'):
            return rss_result

        # Try NewsAPI with demo key as fallback
        demo_result = self._fetch_newsapi_demo(symbol, company_name)
        if demo_result and demo_result.get('articles'):
            return demo_result

        return None

    def _fetch_newsapi_demo(self, symbol, company_name):
        """Încearcă NewsAPI cu demo key gratuit"""
        try:
            # NewsAPI demo key - permite câteva request-uri gratuite pe zi
            demo_key = 'pub_12345678901234567890123456789012345'  # Placeholder - înlocuiește cu un key real dacă ai

            url = 'https://newsdata.io/api/1/news'  # Alternative free news API
            params = {
                'apikey': demo_key,
                'q': f'{company_name} OR {symbol}',
                'language': 'en',
                'size': 20  # Fetch more, then filter
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('results'):
                articles = []
                sentiments = []
                # Filter to ensure articles are relevant to this stock
                keywords = [symbol.lower(), company_name.lower()]

                for item in data['results']:
                    title = item.get('title', '')
                    description = item.get('description', '')
                    article_text = f"{title} {description}".lower()
                    
                    # Only include if article mentions symbol or company
                    if any(keyword in article_text for keyword in keywords):
                        text = f"{title} {description}"
                        polarity = TextBlob(text).sentiment.polarity
                        sentiments.append(polarity)

                        articles.append({
                            'title': title,
                            'description': description or '',
                            'url': item.get('link', ''),
                            'source': item.get('source_id', 'NewsData'),
                            'published_at': item.get('pubDate', ''),
                            'sentiment': polarity
                        })
                        
                        if len(articles) >= 5:
                            break

                if articles:
                    return {'articles': articles, 'sentiments': sentiments}

        except Exception as e:
            print(f"Warning: NewsAPI demo failed for {symbol}: {e}")

        return None

    def _fetch_rss_news(self, symbol, company_name):
        """Obține știri din RSS feeds financiare gratuite"""
        rss_feeds = [
            'https://feeds.finance.yahoo.com/rss/2.0/headline',
            'https://www.investing.com/rss/news.rss',
            'https://feeds.feedburner.com/FinancialTimesMarkets',
            'https://feeds.bloomberg.com/markets/news.rss',
            'https://feeds.marketwatch.com/marketwatch/marketpulse/',
            'https://www.cnbc.com/id/100003114/device/rss/rss.html',
            'https://feeds.reuters.com/reuters/businessNews',
        ]

        try:
            import feedparser
        except ImportError:
            print("feedparser not available, skipping RSS news")
            return None

        articles = []
        sentiments = []

        # Keywords to search for (more flexible matching)
        keywords = [symbol.lower(), company_name.lower()]
        # Add common variations and related terms
        if symbol == 'AAPL':
            keywords.extend(['apple', 'iphone', 'mac', 'tim cook', 'ios', 'ipad'])
        elif symbol == 'GOOGL' or symbol == 'GOOG':
            keywords.extend(['google', 'alphabet', 'android', 'search', 'youtube'])
        elif symbol == 'MSFT':
            keywords.extend(['microsoft', 'windows', 'azure', 'office', 'xbox'])
        elif symbol == 'TSLA':
            keywords.extend(['tesla', 'elon musk', 'electric', 'vehicle', 'ev', 'cybertruck'])
        elif symbol == 'NVDA':
            keywords.extend(['nvidia', 'gpu', 'graphics', 'ai', 'gaming', 'chip'])
        elif symbol == 'AMZN':
            keywords.extend(['amazon', 'ecommerce', 'aws', 'cloud', 'prime'])
        elif symbol == 'META':
            keywords.extend(['facebook', 'instagram', 'whatsapp', 'social media'])

        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)

                for entry in feed.entries[:15]:  # Check more entries per feed
                    title = entry.get('title', '')
                    description = entry.get('description', '')

                    # Check if article is relevant to our symbol/company
                    search_text = f"{title} {description}".lower()

                    # More flexible matching - check if any keyword appears
                    is_relevant = any(keyword in search_text for keyword in keywords)

                    if is_relevant:
                        text = f"{title} {description}"
                        polarity = TextBlob(text).sentiment.polarity
                        sentiments.append(polarity)

                        articles.append({
                            'title': title,
                            'description': description or '',
                            'url': entry.get('link', ''),
                            'source': entry.get('source', {}).get('title', 'Financial News'),
                            'published_at': entry.get('published', ''),
                            'sentiment': polarity
                        })

                        if len(articles) >= 5:
                            break

                if len(articles) >= 5:
                    break

            except Exception as e:
                print(f"Warning: RSS feed {feed_url} failed: {e}")
                continue

        if articles:
            return {'articles': articles[:5], 'sentiments': sentiments[:5]}

        # No company-specific articles found
        print(f"No specific articles found for {symbol}, not returning unrelated general news.")
        return None

    def _fetch_general_financial_news(self):
        """Obține știri financiare generale când nu găsește știri specifice"""
        rss_feeds = [
            'https://feeds.finance.yahoo.com/rss/2.0/headline',
            'https://feeds.bloomberg.com/markets/news.rss',
            'https://feeds.marketwatch.com/marketwatch/marketpulse/',
            'https://www.cnbc.com/id/100003114/device/rss/rss.html',
        ]

        try:
            import feedparser
        except ImportError:
            print("feedparser not available, skipping general financial news")
            return None

        articles = []
        sentiments = []

        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)

                for entry in feed.entries[:20]:  # Get more entries for general news
                    title = entry.get('title', '')
                    description = entry.get('description', '')

                    # Skip articles that are too short or seem like ads/promotions
                    if len(title) < 10 or 'newsletter' in title.lower() or 'subscribe' in title.lower():
                        continue

                    text = f"{title} {description}"
                    polarity = TextBlob(text).sentiment.polarity
                    sentiments.append(polarity)

                    articles.append({
                        'title': title,
                        'description': description or '',
                        'url': entry.get('link', ''),
                        'source': entry.get('source', {}).get('title', 'Financial News'),
                        'published_at': entry.get('published', ''),
                        'sentiment': polarity
                    })

                    if len(articles) >= 5:
                        break

                if len(articles) >= 5:
                    break

            except Exception as e:
                print(f"Warning: General financial RSS feed {feed_url} failed: {e}")
                continue

        if articles:
            return {'articles': articles[:5], 'sentiments': sentiments[:5]}

        return None

    def fetch_sentiment_data(self, symbol, company_name):
        """Obține date de sentiment din news, social media și market correlation"""
        sentiment_data = {
            'news_sentiment': 0,
            'social_sentiment': 0,
            'market_correlation': 0,
            'news_articles': []
        }

        # Fetch news sentiment (cu NewsAPI dacă disponibil)
        valid_articles = []
        valid_sentiments = []

        def set_news(articles, sentiments):
            sentiment_data['news_articles'] = articles
            sentiment_data['news_sentiment'] = sum(sentiments) / len(sentiments) if sentiments else 0

        if self.news_api_key:
            try:
                url = 'https://newsapi.org/v2/everything'
                # Build query with symbol and company name for better relevance
                query = f'({symbol} OR {company_name})'
                params = {
                    'q': query,
                    'apiKey': self.news_api_key,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 20
                }

                response = requests.get(url, params=params, timeout=10)
                news_data = response.json()

                if news_data.get('status') == 'ok' and news_data.get('articles'):
                    # Filter articles to ensure they're actually relevant to this stock
                    keywords = [symbol.lower(), company_name.lower()]
                    for article in news_data['articles']:
                        article_text = f"{article.get('title', '')} {article.get('description', '')}".lower()
                        # Only include if article mentions symbol or company
                        if any(keyword in article_text for keyword in keywords):
                            text = f"{article.get('title', '')} {article.get('description', '')}"
                            polarity = TextBlob(text).sentiment.polarity
                            valid_sentiments.append(polarity)
                            valid_articles.append({
                                'title': article.get('title', ''),
                                'description': article.get('description', ''),
                                'url': article.get('url', ''),
                                'source': article.get('source', {}).get('name', ''),
                                'published_at': article.get('publishedAt', ''),
                                'sentiment': polarity
                            })
                            if len(valid_articles) >= 5:
                                break

                if valid_articles:
                    set_news(valid_articles, valid_sentiments)
                else:
                    raise ValueError('No usable NewsAPI articles')

            except Exception as e:
                print(f"Warning: Error fetching news sentiment for {symbol} from NewsAPI: {e}")
                # Fallback to alternative news sources
                alt_result = self._fetch_alternative_news(symbol, company_name)
                if alt_result and alt_result.get('articles'):
                    print(f"DEBUG: Using alternative news for {symbol} ({len(alt_result['articles'])} articles)")
                    set_news(alt_result['articles'], alt_result['sentiments'])
                else:
                    print(f"DEBUG: All news sources failed for {symbol}, using demo news")
                    sentiment_data['news_sentiment'] = random.uniform(-0.5, 0.8)
                    sentiment_data['news_articles'] = self._generate_demo_news_articles(symbol, company_name)

        else:
            # Try alternative news sources when NewsAPI key is not present
            alt_result = self._fetch_alternative_news(symbol, company_name)
            if alt_result and alt_result.get('articles'):
                print(f"DEBUG: Using alternative news for {symbol} ({len(alt_result['articles'])} articles)")
                set_news(alt_result['articles'], alt_result['sentiments'])
            else:
                print(f"DEBUG: Alternative news not available for {symbol}, using demo fallback")
                sentiment_data['news_sentiment'] = random.uniform(-0.5, 0.8)
                sentiment_data['news_articles'] = self._generate_demo_news_articles(symbol, company_name)
        
        # Fetch social sentiment din StockTwits
        sentiment_data['social_sentiment'] = self._fetch_stocktwits_sentiment(symbol)
        
        # Calculate market correlation
        sentiment_data['market_correlation'] = self._calculate_market_correlation(symbol)
        
        return sentiment_data
    
    def _generate_demo_news_articles(self, symbol, company_name):
        """Generează articole de știri demo pentru fallback"""
        demo_titles = [
            f"{company_name} Reports Strong Q4 Earnings",
            f"Analysts Upgrade {symbol} Stock Rating",
            f"{company_name} Announces New Product Launch",
            f"Market Watch: {symbol} Shows Resilience",
            f"{company_name} CEO Comments on Market Conditions"
        ]
        
        articles = []
        for i, title in enumerate(demo_titles):
            sentiment = random.uniform(-0.3, 0.8)
            articles.append({
                'title': title,
                'description': f"This is a demo news article about {company_name} with sample content for testing purposes.",
                'url': f"https://demo.news/{symbol.lower()}/article-{i+1}",
                'source': 'Demo News',
                'published_at': (datetime.now() - timedelta(hours=i)).isoformat(),
                'sentiment': sentiment
            })
        
        return articles
    
    def _generate_demo_price_data(self, symbol):
        """Generează date simulate de preț"""
        # Base price varies by symbol
        base_prices = {
            'AAPL': 175, 'MSFT': 410, 'GOOGL': 140, 'AMZN': 175,
            'NVDA': 880, 'TSLA': 175, 'META': 485, 'JPM': 195,
            'V': 270, 'WMT': 165, 'DIS': 112, 'NFLX': 610,
            'PYPL': 62, 'INTC': 43, 'AMD': 185, 'BA': 210,
            'NKE': 105, 'MCD': 295, 'KO': 61, 'PEP': 170
        }
        
        base_price = base_prices.get(symbol, 100)
        current_price = base_price * random.uniform(0.95, 1.05)
        previous_close = current_price * random.uniform(0.97, 1.03)
        
        return {
            'current_price': round(current_price, 2),
            'previous_close': round(previous_close, 2),
            'volume': random.randint(10000000, 100000000),
        }
    
    def _generate_demo_technical_data(self, symbol):
        """Generează indicatori tehnici simulați"""
        return {
            'rsi': round(random.uniform(25, 75), 2),
            'macd': round(random.uniform(-2, 2), 4),
            'macd_signal': round(random.uniform(-2, 2), 4),
            'sma_50': round(random.uniform(90, 110), 2),
            'sma_200': round(random.uniform(85, 115), 2),
            'avg_volume': random.randint(20000000, 80000000),
        }
    
    def _generate_demo_fundamental_data(self, symbol):
        """Generează date fundamentale simulate"""
        return {
            'pe_ratio': round(random.uniform(10, 45), 2),
            'eps': round(random.uniform(2, 15), 2),
            'eps_growth': round(random.uniform(-10, 25), 2),
            'revenue_growth': round(random.uniform(-5, 20), 2),
            'debt_to_equity': round(random.uniform(0.2, 2.5), 2),
            'market_cap': random.randint(50000000000, 3000000000000),
        }
    
    def _generate_demo_sentiment_data(self, symbol):
        """Generează date de sentiment simulate"""
        # Creează pattern-uri realiste de sentiment
        sentiment_bias = random.choice([-0.3, 0, 0.3, 0.5])  # Unele acțiuni mai bullish
        
        return {
            'news_sentiment': round(random.uniform(-0.5, 0.8) + sentiment_bias, 3),
            'social_sentiment': round(random.uniform(-0.4, 0.9) + sentiment_bias, 3),
            'market_correlation': round(random.uniform(-0.2, 0.9), 3),
        }
    
    def fetch_essential_data(self, symbol, company_name):
        """Obține doar datele esențiale (preț și indicatori tehnici) pentru batch updates
        Evită rate limiting prin omiterea datelor sentimentului și fundamentale
        """
        print(f"Fetching essential data for {symbol}...")
        
        price_data = self.fetch_price_data(symbol)
        technical_data = self.fetch_technical_indicators(symbol)
        
        return {
            **price_data,
            **technical_data
        }
    
    def fetch_all_data(self, symbol, company_name):
        """Obține toate datele pentru o acțiune"""
        print(f"Fetching data for {symbol}...")
        
        price_data = self.fetch_price_data(symbol)
        technical_data = self.fetch_technical_indicators(symbol)
        fundamental_data = self.fetch_fundamental_data(symbol)
        sentiment_data = self.fetch_sentiment_data(symbol, company_name)
        
        return {
            **price_data,
            **technical_data,
            **fundamental_data,
            **sentiment_data
        }
