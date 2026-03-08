const grid = document.getElementById('grid');
const timestamp = document.getElementById('timestamp');
const refreshBtn = document.getElementById('refreshBtn');

// get category from URL
const params = new URLSearchParams(window.location.search);
const category = params.get('category') || 'Romania';
const force = params.get('force') === 'true';

// set timestamp
if (timestamp) {
    const now = new Date();
    timestamp.textContent = `Last updated: ${now.toLocaleDateString()} at ${now.toLocaleTimeString()}`;
}

// section class mapping
const sectionClasses = {
    'hacker news': 'hacker-news',
    'dev.to': 'devto',
    'lobste.rs': 'lobsters',
};

function getSectionClass(key) {
    if (sectionClasses[key]) return sectionClasses[key];
    if (key.includes('guardian')) return 'guardian';
    return '';
}

function formatDate(publishedAt) {
    if (!publishedAt) return '';
    return `· ${publishedAt.slice(0, 10)} at ${publishedAt.slice(11, 16)}`;
}

function createSection(key, articles) {
    const div = document.createElement('div');
    div.className = `section ${getSectionClass(key)}`;
    div.id = `section-${key.replace(/[^a-z0-9]/gi, '-')}`;

    if (!articles || articles.length === 0) {
        div.innerHTML = `<h2>${key}</h2><p class="no-articles">No articles available right now.</p>`;
        return div;
    }

    const articlesHtml = articles.map(a => `
        <div class="article">
            <a href="${a.url}" target="_blank">${a.title}</a>
            <div class="source">
                ${a.source?.name || ''}
                ${formatDate(a.publishedAt)}
            </div>
        </div>
    `).join('');

    div.innerHTML = `<h2>${key}</h2>${articlesHtml}`;

    // animate in
    div.style.opacity = '0';
    div.style.transform = 'translateY(12px)';
    requestAnimationFrame(() => {
        div.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        div.style.opacity = '1';
        div.style.transform = 'translateY(0)';
    });

    return div;
}

// connect to SSE stream
const url = `/stream?category=${encodeURIComponent(category)}&force=${force}`;
const evtSource = new EventSource(url);

evtSource.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.done) {
        evtSource.close();

        // update timestamp
        const now = new Date();
        if (timestamp) {
            timestamp.textContent = `Last updated: ${now.toLocaleDateString()} at ${now.toLocaleTimeString()}`;
        }

        // remove loading indicator
        const loading = document.getElementById('stream-loading');
        if (loading) loading.remove();
        return;
    }

    // remove placeholder if exists
    const loading = document.getElementById('stream-loading');
    if (loading) loading.remove();

    // append new section to grid
    const section = createSection(data.key, data.articles);
    grid.appendChild(section);
};

evtSource.onerror = function() {
    evtSource.close();
    const loading = document.getElementById('stream-loading');
    if (loading) loading.innerHTML = '<p class="no-results">Error loading news. Please refresh.</p>';
};

// refresh button
if (refreshBtn) {
    refreshBtn.addEventListener('click', function(e) {
        e.preventDefault();
        // redirect with force=true
        const newUrl = `/?category=${encodeURIComponent(category)}&force=true`;
        window.location.href = newUrl;
    });
}