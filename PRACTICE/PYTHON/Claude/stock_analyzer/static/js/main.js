// Stock Market Analyzer - Main JavaScript

let stocks = [];
let filteredStocks = [];
let currentPage = 1;
let totalPages = 1;
let perPage = 500; // fetch enough items so searches find symbols in all pages

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadStocks();
    loadSectors();
    loadStats();
    
    // Setup filters
    setupFilters();
    
    // Setup refresh button
    document.getElementById('refreshBtn').addEventListener('click', refreshData);
    
    // Auto-refresh every 5 minutes
    setInterval(loadStocks, 300000);
});

// Load all stocks
async function loadStocks(page = 1) {
    try {
        const params = new URLSearchParams({
            sentiment: document.getElementById('sentimentFilter').value,
            sector: document.getElementById('sectorFilter').value,
            min_score: document.getElementById('minScore').value,
            sort_by: document.getElementById('sortBy').value,
            order: document.getElementById('sortOrder').value,
            include_delisted: document.getElementById('showDelistedSwitch').checked,
            page: page,
            per_page: perPage
        });
        
        const response = await fetch(`/api/stocks?${params}`);
        const data = await response.json();
        
        stocks = data.stocks;
        filteredStocks = stocks;
        currentPage = data.page || 1;
        totalPages = data.total_pages || 1;
        
        renderStocksTable();
        renderPagination(data);
        updateLastUpdateTime(data.last_update);
        updateStockCount(data.total_count);
        
    } catch (error) {
        console.error('Error loading stocks:', error);
        showError('Failed to load stocks data');
    }
}

// Load available sectors
async function loadSectors() {
    try {
        const response = await fetch('/api/sectors');
        const data = await response.json();
        
        const sectorFilter = document.getElementById('sectorFilter');
        data.sectors.forEach(sector => {
            const option = document.createElement('option');
            option.value = sector;
            option.textContent = sector;
            sectorFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading sectors:', error);
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        document.getElementById('bullishCount').textContent = data.bullish_count;
        document.getElementById('neutralCount').textContent = data.neutral_count;
        document.getElementById('bearishCount').textContent = data.bearish_count;
        document.getElementById('avgScore').textContent = data.average_score.toFixed(1);
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Render stocks table
function renderStocksTable() {
    const tbody = document.getElementById('stocksTableBody');
    
    if (filteredStocks.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="14" class="text-center text-muted">
                    No stocks found matching your criteria
                </td>
            </tr>
        `;
        return;
    }
    
    const rows = filteredStocks.map(stock => {
        const changeClass = stock.daily_change_percent >= 0 ? 'price-up' : 'price-down';
        const changeIcon = stock.daily_change_percent >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';
        
        const scoreClass = getScoreClass(stock.total_score);
        const sentimentBadge = getSentimentBadge(stock.sentiment_class);
        const recoBadge = getRecoBadge(stock.recommendation);
        
        return `
            <tr class="fade-in">
                <td><strong>${stock.symbol}</strong></td>
                <td>${stock.company_name || 'N/A'} ${stock.is_delisted ? '<span class="badge bg-danger ms-1">Delisted</span>' : ''}</td>
                <td><small>${stock.sector || 'N/A'}</small></td>
                <td><strong>$${stock.current_price?.toFixed(2) || 'N/A'}</strong></td>
                <td class="${changeClass}">
                    <i class="fas ${changeIcon}"></i>
                    ${stock.daily_change_percent?.toFixed(2) || '0.00'}%
                </td>
                <td class="text-success"><strong>$${stock.target_price?.toFixed(2) || 'N/A'}</strong></td>
                <td class="text-danger"><strong>$${stock.stop_loss?.toFixed(2) || 'N/A'}</strong></td>
                <td>
                    <span class="score-badge score-${scoreClass}">
                        ${stock.total_score?.toFixed(1) || '0'}
                    </span>
                </td>
                <td><small>${stock.sentiment_score?.toFixed(1) || '0'}</small></td>
                <td><small>${stock.technical_score?.toFixed(1) || '0'}</small></td>
                <td><small>${stock.fundamental_score?.toFixed(1) || '0'}</small></td>
                <td>
                    <span class="badge ${sentimentBadge}">
                        ${stock.sentiment_class || 'N/A'}
                    </span>
                </td>
                <td>
                    <span class="badge ${recoBadge}">
                        ${stock.recommendation || 'N/A'}
                    </span>
                </td>
                <td>
                    <div class="btn-group" role="group">
                        <a href="/stock/${stock.symbol}" class="btn btn-sm btn-outline-primary" title="View Details">
                            <i class="fas fa-chart-line"></i>
                        </a>
                        ${stock.is_delisted ? 
                            `<button class="btn btn-sm btn-outline-success" title="Restore Stock" onclick="restoreStock('${stock.symbol}')">
                                <i class="fas fa-undo"></i>
                            </button>` :
                            `<button class="btn btn-sm btn-outline-warning" title="Mark Delisted" onclick="markDelistedStock('${stock.symbol}')">
                                <i class="fas fa-ban"></i>
                            </button>`
                        }
                        <button class="btn btn-sm btn-outline-danger" title="Delete Stock" onclick="deleteStock('${stock.symbol}')">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
    
    tbody.innerHTML = rows;
}

// Setup filters
function setupFilters() {
    const searchInput = document.getElementById('searchInput');
    const sentimentFilter = document.getElementById('sentimentFilter');
    const sectorFilter = document.getElementById('sectorFilter');
    const minScore = document.getElementById('minScore');
    const sortBy = document.getElementById('sortBy');
    const sortOrder = document.getElementById('sortOrder');
    const showDelistedSwitch = document.getElementById('showDelistedSwitch');
    
    searchInput.addEventListener('input', applyFilters);
    sentimentFilter.addEventListener('change', loadStocks);
    sectorFilter.addEventListener('change', loadStocks);
    minScore.addEventListener('input', debounce(loadStocks, 500));
    sortBy.addEventListener('change', loadStocks);
    sortOrder.addEventListener('change', loadStocks);
    showDelistedSwitch.addEventListener('change', loadStocks);
    
    // Setup quick add stock
    const quickAddBtn = document.getElementById('quickAddBtn');
    if (quickAddBtn) {
        quickAddBtn.addEventListener('click', addQuickStock);
    }
}

// Quick add stock functionality
async function addQuickStock() {
    const symbol = document.getElementById('quickSymbol').value.trim().toUpperCase();
    const companyName = document.getElementById('quickCompany').value.trim();
    const sector = document.getElementById('quickSector').value.trim() || 'Unknown';
    const status = document.getElementById('quickAddStatus');
    
    if (!symbol || !companyName) {
        status.innerHTML = '<div class="alert alert-warning alert-sm">Please enter both symbol and company name.</div>';
        return;
    }
    
    const btn = document.getElementById('quickAddBtn');
    const originalHtml = btn.innerHTML;
    
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Adding...';
    status.innerHTML = '<div class="alert alert-info alert-sm">Adding stock... This may take a few seconds.</div>';
    
    try {
        const response = await fetch('/api/add_stock', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                symbol: symbol,
                company_name: companyName,
                sector: sector
            })
        });
        
        const result = await response.json();
        
        if (response.ok && result.status === 'success') {
            status.innerHTML = `<div class="alert alert-success alert-sm">${result.message}</div>`;
            // Clear form
            document.getElementById('quickSymbol').value = '';
            document.getElementById('quickCompany').value = '';
            document.getElementById('quickSector').value = '';
            // Reload data
            await Promise.all([loadStocks(), loadStats(), loadSectors()]);
        } else {
            status.innerHTML = `<div class="alert alert-danger alert-sm">${result.error || 'Failed to add stock'}</div>`;
        }
    } catch (error) {
        status.innerHTML = `<div class="alert alert-danger alert-sm">Error: ${error.message}</div>`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalHtml;
    }
}

// Apply client-side search filter
function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.trim().toLowerCase();

    if (!searchTerm) {
        filteredStocks = stocks;
        renderStocksTable();
        return;
    }

    filteredStocks = stocks.filter(stock =>
        stock.symbol.toLowerCase().includes(searchTerm) ||
        (stock.company_name && stock.company_name.toLowerCase().includes(searchTerm))
    );

    if (filteredStocks.length === 0 && /^[a-zA-Z]+$/.test(searchTerm)) {
        // If symbol not found in current page, try direct API lookup
        fetch(`/api/stock/${encodeURIComponent(searchTerm.toUpperCase())}`)
            .then(res => res.json())
            .then(data => {
                if (!data.error && data.stock) {
                    filteredStocks = [data.stock];
                }
                renderStocksTable();
            })
            .catch(() => {
                renderStocksTable();
            });
    } else {
        renderStocksTable();
    }
}

// Render pagination controls
function renderPagination(data) {
    // You can add pagination UI here if needed
    console.log(`Page ${data.page} of ${data.total_pages}`);
}

// Update stock count display
function updateStockCount(totalCount) {
    // Add a total count display if you have one in the UI
    console.log(`Total stocks: ${totalCount}`);
}

// Refresh all data
async function refreshData() {
    const btn = document.getElementById('refreshBtn');
    const originalHtml = btn.innerHTML;
    
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    
    try {
        await Promise.all([
            loadStocks(),
            loadStats()
        ]);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalHtml;
    }
}

// Delete stock
async function deleteStock(symbol) {
    if (!confirm(`Are you sure you want to delete ${symbol} from the database?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/delete_stock/${encodeURIComponent(symbol)}`, {
            method: 'DELETE'
        });
        const result = await response.json();

        if (response.ok && result.status === 'success') {
            alert(result.message);
            await Promise.all([loadStocks(), loadStats(), loadSectors()]);
        } else {
            alert(`Error deleting stock: ${result.message || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error deleting stock: ${error.message}`);
    }
}

// Mark stock as delisted
async function markDelistedStock(symbol) {
    if (!confirm(`Are you sure you want to mark ${symbol} as delisted?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/mark_delisted/${encodeURIComponent(symbol)}`, {
            method: 'POST'
        });
        const result = await response.json();

        if (response.ok && result.status === 'success') {
            alert(result.message);
            await Promise.all([loadStocks(), loadStats(), loadSectors()]);
        } else {
            alert(`Error marking delisted: ${result.message || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error marking delisted: ${error.message}`);
    }
}

// Restore delisted stock
async function restoreStock(symbol) {
    if (!confirm(`Are you sure you want to restore ${symbol}?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/restore_stock/${encodeURIComponent(symbol)}`, {
            method: 'POST'
        });
        const result = await response.json();

        if (response.ok && result.status === 'success') {
            alert(result.message);
            await Promise.all([loadStocks(), loadStats(), loadSectors()]);
        } else {
            alert(`Error restoring stock: ${result.message || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error restoring stock: ${error.message}`);
    }
}

// Update last update time
function updateLastUpdateTime(timestamp) {
    if (!timestamp) {
        document.getElementById('lastUpdate').textContent = 'Last update: Never';
        return;
    }
    
    const date = new Date(timestamp);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds
    
    let timeAgo;
    if (diff < 60) {
        timeAgo = 'just now';
    } else if (diff < 3600) {
        timeAgo = `${Math.floor(diff / 60)} minutes ago`;
    } else if (diff < 86400) {
        timeAgo = `${Math.floor(diff / 3600)} hours ago`;
    } else {
        timeAgo = date.toLocaleDateString();
    }
    
    document.getElementById('lastUpdate').textContent = `Last update: ${timeAgo}`;
    
    // Calculate next update time
    calculateNextUpdate();
}

// Calculate next update time
function calculateNextUpdate() {
    const now = new Date();
    const est = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));
    
    const hour = est.getHours();
    const minute = est.getMinutes();
    
    let nextUpdate;
    
    // Pre-market: 6:30 AM EST
    if (hour < 6 || (hour === 6 && minute < 30)) {
        nextUpdate = new Date(est);
        nextUpdate.setHours(6, 30, 0, 0);
    }
    // Post-open: 10:30 AM EST
    else if (hour < 10 || (hour === 10 && minute < 30)) {
        nextUpdate = new Date(est);
        nextUpdate.setHours(10, 30, 0, 0);
    }
    // Tomorrow pre-market
    else {
        nextUpdate = new Date(est);
        nextUpdate.setDate(nextUpdate.getDate() + 1);
        nextUpdate.setHours(6, 30, 0, 0);
    }
    
    const diff = Math.floor((nextUpdate - est) / 1000 / 60); // minutes
    const hours = Math.floor(diff / 60);
    const minutes = diff % 60;
    
    let timeString;
    if (hours > 0) {
        timeString = `${hours}h ${minutes}m`;
    } else {
        timeString = `${minutes}m`;
    }
    
    const element = document.getElementById('nextUpdateTime');
    if (element) {
        element.textContent = timeString;
    }
}

// Helper: Get score class
function getScoreClass(score) {
    if (score >= 75) return 'bullish';
    if (score >= 60) return 'bullish-light';
    if (score >= 40) return 'neutral';
    if (score >= 25) return 'bearish-light';
    return 'bearish';
}

// Helper: Get sentiment badge class
function getSentimentBadge(sentiment) {
    const badges = {
        'Strong Bullish': 'bg-success',
        'Bullish': 'bg-primary',
        'Neutral': 'bg-secondary',
        'Bearish': 'bg-warning text-dark',
        'Strong Bearish': 'bg-danger'
    };
    return badges[sentiment] || 'bg-secondary';
}

// Helper: Get recommendation badge class
function getRecoBadge(reco) {
    const badges = {
        'BUY': 'bg-success',
        'HOLD': 'bg-warning text-dark',
        'SELL': 'bg-danger'
    };
    return badges[reco] || 'bg-secondary';
}

// Helper: Show error message
function showError(message) {
    const tbody = document.getElementById('stocksTableBody');
    tbody.innerHTML = `
        <tr>
            <td colspan="14" class="text-center text-danger">
                <i class="fas fa-exclamation-triangle"></i> ${message}
            </td>
        </tr>
    `;
}

// Helper: Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Update next update time every minute
setInterval(calculateNextUpdate, 60000);
