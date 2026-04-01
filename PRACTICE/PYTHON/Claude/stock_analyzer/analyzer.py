"""
Stock Analysis and Scoring Engine
"""
import random
from datetime import datetime, timedelta
from models import Stock, StockHistory, db

class StockAnalyzer:
    """Analyzer pentru calcularea scorurilor și recomandărilor"""
    
    # Weights for scoring components
    SENTIMENT_WEIGHT = 0.35
    TECHNICAL_WEIGHT = 0.40
    FUNDAMENTAL_WEIGHT = 0.25
    
    # Risk multipliers
    RISK_MULTIPLIER = 1.5
    MAX_STOP_LOSS_PERCENT = 0.15
    
    @staticmethod
    def calculate_sentiment_score(stock):
        """
        Calculează scorul de sentiment (0-100)
        Bazat pe: news sentiment, social media, market correlation
        """
        news_weight = 0.40
        social_weight = 0.30
        market_weight = 0.30
        
        # Normalizare valori la 0-100
        news_score = StockAnalyzer._normalize(stock.news_sentiment, -1, 1) * 100
        social_score = StockAnalyzer._normalize(stock.social_sentiment, -1, 1) * 100
        market_score = StockAnalyzer._normalize(stock.market_correlation, -1, 1) * 100
        
        sentiment_score = (
            news_score * news_weight +
            social_score * social_weight +
            market_score * market_weight
        )
        
        return max(0, min(100, sentiment_score))
    
    @staticmethod
    def calculate_technical_score(stock):
        """
        Calculează scorul tehnic (0-100)
        Bazat pe: RSI, MACD, Moving Averages, Volume
        """
        scores = []
        
        # RSI Score (25%)
        if stock.rsi is not None:
            if stock.rsi < 30:
                rsi_score = 100  # Oversold - bullish
            elif stock.rsi > 70:
                rsi_score = 0    # Overbought - bearish
            else:
                # Linear interpolation
                rsi_score = 100 - ((stock.rsi - 30) / 40 * 100)
            scores.append(rsi_score * 0.25)
        
        # MACD Score (25%)
        if stock.macd is not None and stock.macd_signal is not None:
            macd_diff = stock.macd - stock.macd_signal
            if macd_diff > 0:
                macd_score = 50 + min(macd_diff * 10, 50)  # Bullish
            else:
                macd_score = 50 + max(macd_diff * 10, -50)  # Bearish
            scores.append(macd_score * 0.25)
        
        # Moving Averages Score (30%)
        if stock.current_price and stock.sma_50 and stock.sma_200:
            ma_score = 0
            
            # Golden Cross / Death Cross
            if stock.sma_50 > stock.sma_200:
                ma_score += 40  # Bullish trend
            else:
                ma_score += 10  # Bearish trend
            
            # Price vs SMA50
            if stock.current_price > stock.sma_50:
                ma_score += 30  # Above trend
            else:
                ma_score += 15  # Below trend
            
            # Price vs SMA200
            if stock.current_price > stock.sma_200:
                ma_score += 30  # Long-term uptrend
            
            scores.append(ma_score * 0.30)
        
        # Volume Score (20%)
        if stock.volume and stock.avg_volume:
            volume_ratio = stock.volume / stock.avg_volume
            if volume_ratio > 1.5:
                volume_score = 100  # High volume - strong signal
            elif volume_ratio > 1.0:
                volume_score = 70   # Above average
            elif volume_ratio > 0.7:
                volume_score = 50   # Normal
            else:
                volume_score = 30   # Low volume - weak signal
            scores.append(volume_score * 0.20)
        
        return sum(scores) if scores else 50
    
    @staticmethod
    def calculate_fundamental_score(stock):
        """
        Calculează scorul fundamental (0-100)
        Bazat pe: P/E, EPS Growth, Revenue Growth, Debt-to-Equity
        """
        scores = []
        
        # P/E Ratio Score (30%)
        if stock.pe_ratio is not None and stock.pe_ratio > 0:
            if stock.pe_ratio < 15:
                pe_score = 100  # Undervalued
            elif stock.pe_ratio < 25:
                pe_score = 70   # Fair value
            elif stock.pe_ratio < 40:
                pe_score = 40   # Slightly overvalued
            else:
                pe_score = 20   # Overvalued
            scores.append(pe_score * 0.30)
        
        # EPS Growth Score (25%)
        if stock.eps_growth is not None:
            if stock.eps_growth > 20:
                eps_score = 100  # Excellent growth
            elif stock.eps_growth > 10:
                eps_score = 75   # Good growth
            elif stock.eps_growth > 0:
                eps_score = 50   # Positive growth
            elif stock.eps_growth > -10:
                eps_score = 25   # Slight decline
            else:
                eps_score = 0    # Major decline
            scores.append(eps_score * 0.25)
        
        # Revenue Growth Score (25%)
        if stock.revenue_growth is not None:
            if stock.revenue_growth > 15:
                rev_score = 100  # Strong growth
            elif stock.revenue_growth > 7:
                rev_score = 75   # Good growth
            elif stock.revenue_growth > 0:
                rev_score = 50   # Moderate growth
            elif stock.revenue_growth > -5:
                rev_score = 25   # Slight decline
            else:
                rev_score = 0    # Major decline
            scores.append(rev_score * 0.25)
        
        # Debt-to-Equity Score (20%)
        if stock.debt_to_equity is not None:
            if stock.debt_to_equity < 0.5:
                debt_score = 100  # Very low debt
            elif stock.debt_to_equity < 1.0:
                debt_score = 75   # Healthy debt
            elif stock.debt_to_equity < 2.0:
                debt_score = 50   # Moderate debt
            else:
                debt_score = 25   # High debt
            scores.append(debt_score * 0.20)
        
        return sum(scores) if scores else 50
    
    @staticmethod
    def calculate_total_score(stock):
        """Calculează scorul total bazat pe cele 3 componente"""
        sentiment = StockAnalyzer.calculate_sentiment_score(stock)
        technical = StockAnalyzer.calculate_technical_score(stock)
        fundamental = StockAnalyzer.calculate_fundamental_score(stock)
        
        total = (
            sentiment * StockAnalyzer.SENTIMENT_WEIGHT +
            technical * StockAnalyzer.TECHNICAL_WEIGHT +
            fundamental * StockAnalyzer.FUNDAMENTAL_WEIGHT
        )
        
        return sentiment, technical, fundamental, total
    
    @staticmethod
    def calculate_target_price(stock, total_score):
        """Calculează prețul țintă bazat pe scoring"""
        if not stock.current_price or total_score is None:
            return None
        
        # Expected return bazat pe technical și fundamental
        tech_fund_avg = (stock.technical_score + stock.fundamental_score) / 2
        expected_return = (tech_fund_avg / 100) * StockAnalyzer.RISK_MULTIPLIER
        
        # Bonus pentru sentiment foarte bullish
        if total_score > 75:
            expected_return *= 1.2
        elif total_score > 60:
            expected_return *= 1.1
        
        target_price = stock.current_price * (1 + expected_return)
        return round(target_price, 2)
    
    @staticmethod
    def calculate_stop_loss(stock, total_score):
        """Calculează stop loss bazat pe risc"""
        if not stock.current_price or total_score is None:
            return None
        
        # Risk factor: cu cât scorul e mai mic, cu atât riscul e mai mare
        risk_factor = (100 - total_score) / 100 * StockAnalyzer.MAX_STOP_LOSS_PERCENT
        
        # Minimum 5% stop loss
        risk_factor = max(risk_factor, 0.05)
        
        stop_loss = stock.current_price * (1 - risk_factor)
        return round(stop_loss, 2)
    
    @staticmethod
    def classify_sentiment(total_score):
        """Clasifică sentimentul bazat pe scor"""
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
    
    @staticmethod
    def analyze_stock(stock):
        """Analizează complet o acțiune și actualizează toate valorile"""
        # Calculează scorurile
        sentiment, technical, fundamental, total = StockAnalyzer.calculate_total_score(stock)
        
        # Actualizează scorurile
        stock.sentiment_score = round(sentiment, 2)
        stock.technical_score = round(technical, 2)
        stock.fundamental_score = round(fundamental, 2)
        stock.total_score = round(total, 2)
        
        # Calculează preț țintă și stop loss
        stock.target_price = StockAnalyzer.calculate_target_price(stock, total)
        stock.stop_loss = StockAnalyzer.calculate_stop_loss(stock, total)
        
        # Clasificare
        stock.sentiment_class, stock.recommendation = StockAnalyzer.classify_sentiment(total)
        
        # Calculează daily change
        if stock.current_price and stock.previous_close:
            stock.daily_change_percent = round(
                ((stock.current_price - stock.previous_close) / stock.previous_close) * 100, 2
            )
        
        return stock
    
    @staticmethod
    def save_history(stock):
        """Salvează snapshot-ul curent în istoric pentru grafice"""
        history = StockHistory(
            stock=stock,
            price=stock.current_price,
            total_score=stock.total_score,
            volume=stock.volume,
            recorded_at=datetime.utcnow()
        )
        db.session.add(history)
    
    @staticmethod
    def _normalize(value, min_val, max_val):
        """Normalizează o valoare în range [0, 1]"""
        if value is None:
            return 0.5
        return (value - min_val) / (max_val - min_val)
