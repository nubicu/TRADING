const API = '';

function getToken() { return localStorage.getItem('token'); }
function getUser() { return JSON.parse(localStorage.getItem('user') || 'null'); }

function setAuth(token, user) {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    updateNavbar();
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
}

function updateNavbar() {
    const user = getUser();
    const token = getToken();
    if (token && user) {
        document.getElementById('guestNav')?.classList.add('d-none');
        document.getElementById('userNav')?.classList.remove('d-none');
        const nameEl = document.getElementById('userName');
        if (nameEl) nameEl.textContent = user.full_name?.split(' ')[0] || 'Contul Meu';
    } else {
        document.getElementById('guestNav')?.classList.remove('d-none');
        document.getElementById('userNav')?.classList.add('d-none');
    }
    updateCartBadge();
}

async function apiRequest(endpoint, method = 'GET', body = null, auth = false) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth) {
        const token = getToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;
    }
    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);
    const response = await fetch(API + endpoint, options);
    if (response.status === 401 && auth) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return null;
    }
    return response;
}

async function updateCartBadge() {
    const token = getToken();
    if (!token) { document.getElementById('cartBadge')?.classList.add('d-none'); return; }
    try {
        const res = await apiRequest('/api/cart/', 'GET', null, true);
        if (res && res.ok) {
            const items = await res.json();
            const total = items.reduce((s, i) => s + i.quantity, 0);
            const badge = document.getElementById('cartBadge');
            if (badge) {
                badge.textContent = total;
                total > 0 ? badge.classList.remove('d-none') : badge.classList.add('d-none');
            }
        }
    } catch(e) {}
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('liveToast');
    const msg = document.getElementById('toastMessage');
    if (!toast || !msg) return;
    msg.textContent = message;
    toast.className = `toast align-items-center text-white border-0 bg-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'success'}`;
    new bootstrap.Toast(toast, { delay: 3000 }).show();
}

function handleSearch(e) {
    e.preventDefault();
    const q = document.getElementById('searchInput').value.trim();
    if (q) window.location.href = `/?search=${encodeURIComponent(q)}`;
}

document.addEventListener('DOMContentLoaded', () => {
    updateNavbar();
});