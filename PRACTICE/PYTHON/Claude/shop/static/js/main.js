let currentCategory = '';
let currentSearch = '';

async function loadCategories() {
    try {
        const res = await fetch('/api/products/categories');
        const cats = await res.json();
        const bar = document.getElementById('categoriesBar');
        if (!bar) return;
        cats.forEach(cat => {
            const btn = document.createElement('a');
            btn.href = '#';
            btn.className = 'btn btn-sm btn-outline-secondary category-btn';
            btn.dataset.category = cat.slug;
            btn.textContent = cat.name;
            btn.onclick = (e) => { e.preventDefault(); filterByCategory(cat.slug); };
            bar.appendChild(btn);
        });
    } catch(e) { console.error(e); }
}

function filterByCategory(slug) {
    currentCategory = slug;
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.category === slug);
    });
    loadProducts();
}

async function loadProducts(search = currentSearch) {
    const container = document.getElementById('productsContainer');
    if (!container) return;
    container.innerHTML = '<div class="col-12 text-center py-5"><div class="spinner-border text-primary"></div></div>';
    
    let url = '/api/products/?limit=24';
    if (currentCategory) url += `&category=${currentCategory}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;
    
    try {
        const res = await fetch(url);
        const products = await res.json();
        container.innerHTML = '';
        if (products.length === 0) {
            container.innerHTML = '<div class="col-12 text-center py-5"><i class="fas fa-search fa-3x text-muted mb-3"></i><h5 class="text-muted">Niciun produs găsit</h5></div>';
            return;
        }
        products.forEach(p => container.appendChild(createProductCard(p)));
    } catch(e) {
        container.innerHTML = '<div class="col-12 text-center py-5"><p class="text-danger">Eroare la încărcare</p></div>';
    }
}

function createProductCard(p) {
    const col = document.createElement('div');
    col.className = 'col-6 col-md-4 col-lg-3';
    const discount = p.old_price ? Math.round((1 - p.price / p.old_price) * 100) : 0;
    const stars = generateStars(p.rating);
    col.innerHTML = `
    <div class="product-card h-100" onclick="window.location.href='/produs/${p.id}'">
        <div class="product-img-wrap">
            <img src="${p.image_url || 'https://via.placeholder.com/300x220?text=Produs'}" class="card-img-top" alt="${p.name}" loading="lazy">
            ${discount > 0 ? `<span class="badge-discount">-${discount}%</span>` : ''}
            ${p.is_featured ? '<span class="badge-featured"><i class="fas fa-star me-1"></i>Top</span>' : ''}
        </div>
        <div class="card-body p-3">
            <p class="text-muted small mb-1">${p.category?.name || ''}</p>
            <h6 class="card-title fw-semibold mb-2 product-name-link">${p.name}</h6>
            <div class="d-flex align-items-center gap-1 mb-2">
                <div class="stars">${stars}</div>
                <span class="text-muted small">(${p.reviews_count})</span>
            </div>
            <div class="d-flex align-items-center gap-2 mb-3">
                <span class="price-current">${p.price.toFixed(2)} Lei</span>
                ${p.old_price ? `<span class="price-old">${p.old_price.toFixed(2)} Lei</span>` : ''}
            </div>
            <button class="btn-add-cart" onclick="event.stopPropagation(); addToCart(${p.id}, '${p.name}')">
                <i class="fas fa-cart-plus me-2"></i>Adaugă în coș
            </button>
        </div>
    </div>`;
    return col;
}

function generateStars(rating) {
    let html = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= Math.floor(rating)) html += '<i class="fas fa-star"></i>';
        else if (i - 0.5 <= rating) html += '<i class="fas fa-star-half-alt"></i>';
        else html += '<i class="far fa-star"></i>';
    }
    return html;
}

async function addToCart(productId, productName) {
    const token = getToken();
    if (!token) {
        showToast('Trebuie să fii autentificat pentru a adăuga în coș', 'warning');
        setTimeout(() => window.location.href = '/login', 1500);
        return;
    }
    try {
        const res = await apiRequest(`/api/cart/add?product_id=${productId}&quantity=1`, 'POST', null, true);
        if (res && res.ok) {
            showToast(`"${productName}" adăugat în coș!`);
            updateCartBadge();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Eroare', 'error');
        }
    } catch(e) { showToast('Eroare de conexiune', 'error'); }
}

// Init homepage
document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    currentSearch = params.get('search') || '';
    if (currentSearch) {
        const inp = document.getElementById('searchInput');
        if (inp) inp.value = currentSearch;
    }
    if (document.getElementById('productsContainer')) {
        await loadCategories();
        await loadProducts(currentSearch);
    }
});