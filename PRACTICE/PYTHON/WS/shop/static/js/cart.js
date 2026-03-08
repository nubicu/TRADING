async function loadCart() {
    const token = getToken();
    if (!token) { window.location.href = '/login'; return; }
    
    const container = document.getElementById('cartContainer');
    const summary = document.getElementById('cartSummary');
    container.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-primary"></div></div>';
    
    try {
        const res = await apiRequest('/api/cart/', 'GET', null, true);
        if (!res || !res.ok) return;
        const items = await res.json();
        
        if (items.length === 0) {
            container.innerHTML = `<div class="text-center py-5">
                <i class="fas fa-shopping-cart fa-4x text-muted mb-3"></i>
                <h4 class="text-muted">Coșul tău este gol</h4>
                <a href="/" class="btn btn-primary mt-3">Continuă cumpărăturile</a>
            </div>`;
            summary.innerHTML = '';
            return;
        }
        
        container.innerHTML = '';
        let total = 0;
        items.forEach(item => {
            total += item.product.price * item.quantity;
            container.appendChild(createCartItem(item));
        });
        
        summary.innerHTML = `
        <div class="order-summary">
            <h5 class="fw-bold mb-4">Sumar Comandă</h5>
            <div class="d-flex justify-content-between mb-2">
                <span>Subtotal</span><strong>${total.toFixed(2)} Lei</strong>
            </div>
            <div class="d-flex justify-content-between mb-2">
                <span>Transport</span><strong class="text-success">GRATUIT</strong>
            </div>
            <hr>
            <div class="d-flex justify-content-between mb-4">
                <span class="fw-bold">Total</span><strong class="fs-5 text-primary">${total.toFixed(2)} Lei</strong>
            </div>
            <a href="/checkout" class="btn btn-buy-now w-100 mb-3">
                <i class="fas fa-lock me-2"></i>Finalizează Comanda
            </a>
            <a href="/" class="btn btn-outline-secondary w-100">Continuă cumpărăturile</a>
        </div>`;
    } catch(e) { container.innerHTML = '<p class="text-danger">Eroare la încărcare</p>'; }
}

function createCartItem(item) {
    const div = document.createElement('div');
    div.className = 'cart-item mb-3';
    div.id = `cart-item-${item.id}`;
    div.innerHTML = `
    <div class="d-flex align-items-center gap-3">
        <img src="${item.product.image_url || 'https://via.placeholder.com/80'}" alt="${item.product.name}" onclick="window.location.href='/produs/${item.product.id}'" style="cursor:pointer">
        <div class="flex-grow-1">
            <h6 class="mb-1 fw-semibold" style="cursor:pointer" onclick="window.location.href='/produs/${item.product.id}'">${item.product.name}</h6>
            <p class="text-muted small mb-2">${item.product.category?.name || ''}</p>
            <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                <div class="qty-control">
                    <button class="qty-btn" onclick="changeQty(${item.id}, ${item.quantity - 1})"><i class="fas fa-minus"></i></button>
                    <span class="fw-semibold px-2" id="qty-${item.id}">${item.quantity}</span>
                    <button class="qty-btn" onclick="changeQty(${item.id}, ${item.quantity + 1})"><i class="fas fa-plus"></i></button>
                </div>
                <strong class="text-primary">${(item.product.price * item.quantity).toFixed(2)} Lei</strong>
                <button class="btn btn-sm btn-outline-danger" onclick="removeItem(${item.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    </div>`;
    return div;
}

async function changeQty(itemId, newQty) {
    if (newQty < 1) { removeItem(itemId); return; }
    const res = await apiRequest(`/api/cart/update/${itemId}?quantity=${newQty}`, 'PUT', null, true);
    if (res && res.ok) { loadCart(); updateCartBadge(); }
}

async function removeItem(itemId) {
    const res = await apiRequest(`/api/cart/remove/${itemId}`, 'DELETE', null, true);
    if (res && res.ok) { loadCart(); updateCartBadge(); showToast('Produs eliminat din coș'); }
}