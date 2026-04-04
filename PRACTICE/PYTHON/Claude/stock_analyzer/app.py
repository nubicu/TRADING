"""
Stock Market Analyzer - Flask Application
"""
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import os
import time
import json

from models import db, Stock, UpdateLog, StockHistory
from analyzer import StockAnalyzer
from data_fetcher import DataFetcher

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize database
db.init_app(app)

# Initialize data fetcher
data_fetcher = DataFetcher()


@app.route('/')
def index():
    """Dashboard principal"""
    return render_template('index.html')


@app.route('/stock/<symbol>')
def stock_detail(symbol):
    """Pagină detalii pentru o acțiune"""
    return render_template('stock_detail.html', symbol=symbol)


@app.route('/settings')
def settings():
    """Pagină setări"""
    return render_template('settings.html')


# ==================== API ENDPOINTS ====================

@app.route('/api/stocks')
def get_stocks():
    """Returnează toate acțiunile cu scoring - cu suport pentru paginare"""
    # Parametri de filtrare și sortare
    sentiment_filter = request.args.get('sentiment')
    min_score = request.args.get('min_score', 65, type=float)
    max_score = request.args.get('max_score', type=float)
    sector = request.args.get('sector')
    sort_by = request.args.get('sort_by', 'total_score')
    order = request.args.get('order', 'desc')
    
    # Paginare
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 100, type=int)
    per_page = min(per_page, 500)  # Max 500 per page
    
    # Query de bază
    query = Stock.query
    include_delisted = request.args.get('include_delisted', 'false').lower() == 'true'
    if not include_delisted:
        query = query.filter(Stock.is_delisted == False)
    
    # Aplicare filtre
    if sentiment_filter:
        query = query.filter(Stock.sentiment_class == sentiment_filter)
    
    if min_score is not None:
        query = query.filter(Stock.total_score >= min_score)
    
    if max_score is not None:
        query = query.filter(Stock.total_score <= max_score)
    
    if sector:
        query = query.filter(Stock.sector == sector)
    
    # Sortare
    if hasattr(Stock, sort_by):
        sort_column = getattr(Stock, sort_by)
        if order == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    
    # Paginare
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    stocks = pagination.items
    
    # Get last update info
    last_log = UpdateLog.query.order_by(UpdateLog.created_at.desc()).first()
    last_update = last_log.created_at.isoformat() if last_log else None
    
    return jsonify({
        'stocks': [stock.to_dict() for stock in stocks],
        'total_count': pagination.total,
        'page': page,
        'per_page': per_page,
        'total_pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'last_update': last_update,
        'filters_applied': {
            'sentiment': sentiment_filter,
            'min_score': min_score,
            'max_score': max_score,
            'sector': sector,
            'sort_by': sort_by,
            'order': order
        }
    })


@app.route('/api/stock/<symbol>')
def get_stock(symbol):
    """Detalii complete pentru o acțiune"""
    symbol_clean = symbol.strip().upper()
    stock = Stock.query.filter_by(symbol=symbol_clean).first()
    
    if not stock:
        return jsonify({'error': 'Stock not found'}), 404

    # Determine if we need to refresh details (once per day)
    now = datetime.utcnow()
    today = now.date()
    news_articles = []

    if not stock.last_detail_fetched or stock.last_detail_fetched.date() < today:
        # Update technical, fundamental and sentiment data only once per day when opening detail page
        try:
            tech_data = data_fetcher.fetch_technical_indicators(symbol)
            fund_data = data_fetcher.fetch_fundamental_data(symbol)
            sentiment_data = data_fetcher.fetch_sentiment_data(symbol, stock.company_name)

            for key, value in {**tech_data, **fund_data, **sentiment_data}.items():
                if hasattr(stock, key) and value is not None:
                    setattr(stock, key, value)

            news_articles = sentiment_data.get('news_articles', [])
            stock.cached_news = json.dumps(news_articles)
            stock.last_detail_fetched = now
            db.session.commit()

            print(f"DEBUG: Refreshed stock details for {symbol} at {now.isoformat()}")
        except Exception as e:
            print(f"Warning: Could not refresh stock details for {symbol}: {e}")
            # fallback to cached news from DB if available
            try:
                news_articles = json.loads(stock.cached_news) if stock.cached_news else []
            except Exception:
                news_articles = []
    else:
        try:
            news_articles = json.loads(stock.cached_news) if stock.cached_news else []
        except Exception:
            news_articles = []

    # Get historical data for charts (last 30 days)
    history = StockHistory.query.filter_by(stock_id=stock.id)\
        .filter(StockHistory.recorded_at >= datetime.utcnow() - timedelta(days=30))\
        .order_by(StockHistory.recorded_at.asc())\
        .all()
    
    return jsonify({
        'stock': stock.to_dict(),
        'history': [{
            'date': h.recorded_at.isoformat(),
            'price': h.price,
            'score': h.total_score,
            'volume': h.volume
        } for h in history],
        'news': news_articles
    })


@app.route('/api/sectors')
def get_sectors():
    """Returnează toate sectoarele disponibile"""
    sectors = db.session.query(Stock.sector).distinct().all()
    return jsonify({
        'sectors': [s[0] for s in sectors if s[0]]
    })


@app.route('/api/update', methods=['POST'])
def trigger_update():
    """Trigger manual pentru update-ul datelor cu batch processing
    Batch size = 50 tickere, delay 5 secunde între batch-uri
    Folosește doar date esențiale (preț + indicatori tehnici) pentru a evita rate limiting
    """
    start_time = datetime.utcnow()
    update_type = request.json.get('update_type', 'manual') if request.json else 'manual'
    batch_size = 50  # Fixed batch size pentru rate limiting optimal
    
    try:
        print(f"\n{'='*60}")
        print(f"🔄 Starting {update_type} update at {start_time}")
        print(f"{'='*60}\n")
        
        # Get stock list
        stock_list = data_fetcher.get_stock_list()
        total_stocks = len(stock_list)
        updated_count = 0
        error_count = 0
        
        print(f"📊 Processing {total_stocks} stocks in batches of {batch_size}...")
        
        # Process in batches
        for i in range(0, total_stocks, batch_size):
            batch = stock_list[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_stocks + batch_size - 1) // batch_size
            
            print(f"\n🔄 Batch {batch_num}/{total_batches} ({len(batch)} stocks)...")
            
            for idx, (symbol, company_name, sector) in enumerate(batch):
                try:
                    # Add small delay between stocks in batch to avoid rate limiting
                    if idx > 0:
                        time.sleep(0.2)  # 200ms between stock fetches in batch
                    
                    # Fetch only essential data (price + technical indicators)
                    # Sentiment and fundamental data are fetched only on detail page view
                    data = data_fetcher.fetch_essential_data(symbol, company_name)
                    
                    # Get or create stock
                    stock = Stock.query.filter_by(symbol=symbol).first()
                    if not stock:
                        stock = Stock(
                            symbol=symbol,
                            company_name=company_name,
                            sector=sector
                        )
                        db.session.add(stock)
                    
                    # Update stock data (do not overwrite existing values with None)
                    for key, value in data.items():
                        if hasattr(stock, key) and value is not None:
                            setattr(stock, key, value)
                    
                    # Analyze and calculate scores
                    stock = StockAnalyzer.analyze_stock(stock)
                    
                    # Save to history
                    StockAnalyzer.save_history(stock)
                    
                    updated_count += 1
                    
                    # Show progress every 10 stocks
                    if updated_count % 10 == 0:
                        print(f"  ✓ {updated_count}/{total_stocks} stocks processed...")
                    
                except Exception as e:
                    error_count += 1
                    if error_count <= 5:  # Only show first 5 errors
                        print(f"  ✗ Error updating {symbol}: {str(e)}")
                    continue
            
            # Commit batch
            try:
                db.session.commit()
                print(f"  💾 Batch {batch_num} committed to database")
            except Exception as e:
                print(f"  ❌ Error committing batch {batch_num}: {str(e)}")
                db.session.rollback()
            
            # Add delay between batches to let rate limits reset
            if batch_num < total_batches:
                print(f"  ⏳ Waiting 5 seconds before next batch...")
                time.sleep(5)
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Log update
        log = UpdateLog(
            update_type=update_type,
            start_time=start_time,
            end_time=end_time,
            stocks_updated=updated_count,
            status='success' if updated_count > 0 else 'failed'
        )
        db.session.add(log)
        db.session.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ Update completed!")
        print(f"📊 Updated: {updated_count}/{len(stock_list)} stocks")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"{'='*60}\n")
        
        return jsonify({
            'status': 'success',
            'updated_stocks': updated_count,
            'total_stocks': len(stock_list),
            'duration': duration,
            'update_type': update_type
        })
        
    except Exception as e:
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Log failed update
        log = UpdateLog(
            update_type=update_type,
            start_time=start_time,
            end_time=end_time,
            stocks_updated=0,
            status='failed',
            error_message=str(e)
        )
        db.session.add(log)
        db.session.commit()
        
        print(f"\n❌ Update failed: {str(e)}\n")
        
        return jsonify({
            'status': 'error',
            'message': str(e),
            'duration': duration
        }), 500


@app.route('/api/delete_stock/<symbol>', methods=['DELETE'])
def delete_stock(symbol):
    """Șterge un ticker din baza de date"""
    symbol_clean = symbol.strip().upper()
    stock = Stock.query.filter_by(symbol=symbol_clean).first()
    if not stock:
        return jsonify({'status': 'error', 'message': f'Stock {symbol_clean} not found'}), 404

    try:
        # Delete related history first (if exists)
        StockHistory.query.filter_by(stock_id=stock.id).delete()
        db.session.delete(stock)
        db.session.commit()

        return jsonify({'status': 'success', 'message': f'Stock {symbol_clean} deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Failed to delete {symbol_clean}: {str(e)}'}), 500


@app.route('/api/mark_delisted/<symbol>', methods=['POST'])
def mark_delisted(symbol):
    """Marchează un ticker ca delistat (păstrează istoricul)"""
    symbol_clean = symbol.strip().upper()
    stock = Stock.query.filter_by(symbol=symbol_clean).first()
    if not stock:
        return jsonify({'status': 'error', 'message': f'Stock {symbol_clean} not found'}), 404

    try:
        stock.is_delisted = True
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'Stock {symbol_clean} marked as delisted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Failed to mark delisted {symbol_clean}: {str(e)}'}), 500


@app.route('/api/restore_stock/<symbol>', methods=['POST'])
def restore_stock(symbol):
    """Reactivează un ticker din delistare"""
    symbol_clean = symbol.strip().upper()
    stock = Stock.query.filter_by(symbol=symbol_clean).first()
    if not stock:
        return jsonify({'status': 'error', 'message': f'Stock {symbol_clean} not found'}), 404

    try:
        stock.is_delisted = False
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'Stock {symbol_clean} restored'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Failed to restore {symbol_clean}: {str(e)}'}), 500


@app.route('/api/stats')
def get_stats():
    """Statistici generale"""
    total_stocks = Stock.query.count()
    bullish = Stock.query.filter(Stock.total_score >= 60).count()
    bearish = Stock.query.filter(Stock.total_score < 40).count()
    
    avg_score = db.session.query(db.func.avg(Stock.total_score)).scalar() or 0
    
    # Top performers
    top_stocks = Stock.query.order_by(Stock.total_score.desc()).limit(5).all()
    
    # Recent updates
    recent_logs = UpdateLog.query.order_by(UpdateLog.created_at.desc()).limit(10).all()
    
    return jsonify({
        'total_stocks': total_stocks,
        'bullish_count': bullish,
        'bearish_count': bearish,
        'neutral_count': total_stocks - bullish - bearish,
        'average_score': round(avg_score, 2),
        'top_performers': [stock.to_dict() for stock in top_stocks],
        'recent_updates': [{
            'type': log.update_type,
            'time': log.created_at.isoformat(),
            'stocks_updated': log.stocks_updated,
            'status': log.status
        } for log in recent_logs]
    })


@app.route('/api/history/<symbol>')
def get_history(symbol):
    """Istoric pentru o acțiune (pentru grafice)"""
    days = request.args.get('days', 30, type=int)
    
    stock = Stock.query.filter_by(symbol=symbol.upper()).first()
    if not stock:
        return jsonify({'error': 'Stock not found'}), 404
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    history = StockHistory.query.filter_by(stock_id=stock.id)\
        .filter(StockHistory.recorded_at >= cutoff_date)\
        .order_by(StockHistory.recorded_at.asc())\
        .all()
    
    return jsonify({
        'symbol': symbol,
        'history': [{
            'date': h.recorded_at.isoformat(),
            'price': h.price,
            'score': h.total_score,
            'volume': h.volume
        } for h in history]
    })


@app.route('/api/add_stock', methods=['POST'])
def add_stock():
    """Adaugă o nouă acțiune în baza de date"""
    data = request.get_json()
    symbol = data.get('symbol', '').strip().upper()
    company_name = data.get('company_name', '').strip()
    sector = data.get('sector', 'Unknown').strip()

    if not symbol or not company_name:
        return jsonify({'error': 'Symbol and company name are required'}), 400

    # Check if stock already exists
    existing_stock = Stock.query.filter_by(symbol=symbol).first()
    if existing_stock:
        return jsonify({'error': f'Stock {symbol} already exists'}), 409

    try:
        print(f"Adding new stock: {symbol} - {company_name}")

        # Create new stock
        stock = Stock(
            symbol=symbol,
            company_name=company_name,
            sector=sector
        )
        db.session.add(stock)

        # Fetch data
        stock_data = data_fetcher.fetch_all_data(symbol, company_name)

        # Update stock with fetched data
        for key, value in stock_data.items():
            if hasattr(stock, key) and value is not None:
                setattr(stock, key, value)

        # Analyze and calculate scores
        stock = StockAnalyzer.analyze_stock(stock)

        # Save to history
        StockAnalyzer.save_history(stock)

        # Commit to database
        db.session.commit()

        print(f"✅ Successfully added {symbol}")

        return jsonify({
            'status': 'success',
            'stock': stock.to_dict(),
            'message': f'Stock {symbol} added successfully'
        })

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error adding {symbol}: {str(e)}")
        return jsonify({
            'error': f'Failed to add stock {symbol}: {str(e)}'
        }), 500


def init_database():

    """Initialize database și populează cu date inițiale"""
    with app.app_context():
        # Create tables only if they don't exist
        db.create_all()
        
        # Check if we need to populate
        stock_count = Stock.query.count()
        if stock_count == 0:
            print("📊 Database is empty. Run manual update from Dashboard or use reset_db.py")
        else:
            print(f"✅ Database already contains {stock_count} stocks")


if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    
    # Run Flask app
    print("\n" + "="*60)
    print("🚀 Starting Stock Market Analyzer")
    print("="*60)
    print(f"📍 Server: http://localhost:5000")
    print(f"📊 Dashboard: http://localhost:5000")
    print(f"⚙️  Settings: http://localhost:5000/settings")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
