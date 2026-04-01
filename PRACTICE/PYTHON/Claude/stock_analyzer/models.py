"""
Database models for Stock Market Analyzer
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Stock(db.Model):
    """Model pentru stocarea informațiilor despre acțiuni"""
    __tablename__ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False, index=True)
    company_name = db.Column(db.String(200))
    sector = db.Column(db.String(100))
    
    # Preț și variație
    current_price = db.Column(db.Float)
    previous_close = db.Column(db.Float)
    daily_change_percent = db.Column(db.Float)
    target_price = db.Column(db.Float)
    stop_loss = db.Column(db.Float)
    
    # Scoring components
    sentiment_score = db.Column(db.Float, default=0)
    technical_score = db.Column(db.Float, default=0)
    fundamental_score = db.Column(db.Float, default=0)
    total_score = db.Column(db.Float, default=0)
    
    # Sentiment indicators
    news_sentiment = db.Column(db.Float)
    social_sentiment = db.Column(db.Float)
    market_correlation = db.Column(db.Float)
    
    # Technical indicators
    rsi = db.Column(db.Float)
    macd = db.Column(db.Float)
    macd_signal = db.Column(db.Float)
    sma_50 = db.Column(db.Float)
    sma_200 = db.Column(db.Float)
    volume = db.Column(db.BigInteger)
    avg_volume = db.Column(db.BigInteger)
    
    # Fundamental indicators
    pe_ratio = db.Column(db.Float)
    eps = db.Column(db.Float)
    eps_growth = db.Column(db.Float)
    revenue_growth = db.Column(db.Float)
    debt_to_equity = db.Column(db.Float)
    market_cap = db.Column(db.BigInteger)
    
    # Classification
    sentiment_class = db.Column(db.String(20))  # Strong Bullish, Bullish, etc.
    recommendation = db.Column(db.String(20))   # BUY, HOLD, SELL

    # Delisting flag
    is_delisted = db.Column(db.Boolean, default=False, nullable=False)

    # Detail page caching
    last_detail_fetched = db.Column(db.DateTime, nullable=True)
    cached_news = db.Column(db.Text, nullable=True)
    
    # Timestamps
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Stock {self.symbol}>'
    
    def to_dict(self):
        """Convertește obiectul în dicționar pentru JSON"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'sector': self.sector,
            'current_price': round(self.current_price, 2) if self.current_price else None,
            'previous_close': round(self.previous_close, 2) if self.previous_close else None,
            'daily_change_percent': round(self.daily_change_percent, 2) if self.daily_change_percent else None,
            'target_price': round(self.target_price, 2) if self.target_price else None,
            'stop_loss': round(self.stop_loss, 2) if self.stop_loss else None,
            'sentiment_score': round(self.sentiment_score, 2) if self.sentiment_score else 0,
            'technical_score': round(self.technical_score, 2) if self.technical_score else 0,
            'fundamental_score': round(self.fundamental_score, 2) if self.fundamental_score else 0,
            'total_score': round(self.total_score, 2) if self.total_score else 0,
            'sentiment_class': self.sentiment_class,
            'recommendation': self.recommendation,
            'rsi': round(self.rsi, 2) if self.rsi else None,
            'macd': round(self.macd, 4) if self.macd else None,
            'macd_signal': round(self.macd_signal, 4) if self.macd_signal else None,
            'sma_50': round(self.sma_50, 2) if self.sma_50 else None,
            'sma_200': round(self.sma_200, 2) if self.sma_200 else None,
            'volume': self.volume,
            'avg_volume': self.avg_volume,
            'pe_ratio': round(self.pe_ratio, 2) if self.pe_ratio else None,
            'eps': round(self.eps, 2) if self.eps else None,
            'eps_growth': round(self.eps_growth, 2) if self.eps_growth else None,
            'revenue_growth': round(self.revenue_growth, 2) if self.revenue_growth else None,
            'debt_to_equity': round(self.debt_to_equity, 2) if self.debt_to_equity else None,
            'market_cap': self.market_cap,
            'news_sentiment': round(self.news_sentiment, 3) if self.news_sentiment else None,
            'social_sentiment': round(self.social_sentiment, 3) if self.social_sentiment else None,
            'market_correlation': round(self.market_correlation, 3) if self.market_correlation else None,
            'is_delisted': self.is_delisted,
            'last_detail_fetched': self.last_detail_fetched.isoformat() if self.last_detail_fetched else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }


class UpdateLog(db.Model):
    """Log pentru update-uri automate"""
    __tablename__ = 'update_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    update_type = db.Column(db.String(50))  # pre_market, post_open
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    stocks_updated = db.Column(db.Integer)
    status = db.Column(db.String(20))  # success, failed, partial
    error_message = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UpdateLog {self.update_type} at {self.created_at}>'


class StockHistory(db.Model):
    """Istoric prețuri și scoruri pentru grafice"""
    __tablename__ = 'stock_history'
    
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    
    price = db.Column(db.Float)
    total_score = db.Column(db.Float)
    volume = db.Column(db.BigInteger)
    
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    stock = db.relationship('Stock', backref=db.backref('history', lazy='dynamic'))
    
    def __repr__(self):
        return f'<StockHistory {self.stock_id} at {self.recorded_at}>'
