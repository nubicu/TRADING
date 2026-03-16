/* script.js */
document.addEventListener('DOMContentLoaded', () => {
    const storyList = document.getElementById('storyList');
    const welcomeMessage = document.getElementById('welcomeMessage');
    const storyViewer = document.getElementById('storyViewer');
    const storyContent = document.getElementById('storyContent');
    const searchInput = document.getElementById('searchInput');
    const storyCount = document.getElementById('storyCount');
    const backToTopBtn = document.getElementById('backToTopBtn');

    let allStories = [];

    // Funcția pentru scroll sus în zona de vizualizare (Fixată)
    const scrollToTop = () => {
        storyViewer.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // Atașare eveniment la butonul de scroll
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', scrollToTop);
    }

    const init = () => {
        if (typeof storyData !== 'undefined') {
            allStories = storyData;
            renderList(allStories);
            storyCount.textContent = allStories.length;
        } else {
            console.error('Data poveștilor nu a putut fi încărcată.');
        }
    };

    const renderList = (stories) => {
        storyList.innerHTML = '';
        stories.forEach((story, index) => {
            const button = document.createElement('button');
            button.className = 'list-group-item list-group-item-action';
            button.innerHTML = `<i class="fa-solid fa-chevron-right me-2 small text-info"></i> ${story.title}`;
            
            button.addEventListener('click', () => {
                // Marcare element activ
                document.querySelectorAll('.list-group-item').forEach(el => el.classList.remove('active'));
                button.classList.add('active');
                
                // Afișare poveste
                displayStory(story);
            });
            
            storyList.appendChild(button);
        });
    };

    const displayStory = (story) => {
        welcomeMessage.classList.add('d-none');
        storyViewer.classList.remove('d-none');
        
        // Randare Markdown în HTML folosind library-ul 'marked'
        if (typeof marked !== 'undefined') {
            storyContent.innerHTML = marked.parse(story.content);
        } else {
            // Fallback dacă marked nu s-a încărcat
            storyContent.innerHTML = `<h2>${story.title}</h2><p>${story.content.replace(/\n/g, '<br>')}</p>`;
        }
        
        // Resetare poziție scroll la începutul noii povești
        storyViewer.scrollTop = 0;
    };

    const handleSearch = () => {
        const term = searchInput.value.toLowerCase().trim();
        const filtered = allStories.filter(story => 
            story.title.toLowerCase().includes(term) || 
            story.content.toLowerCase().includes(term)
        );
        renderList(filtered);
    };

    searchInput.addEventListener('input', debounce(handleSearch, 300));

    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    init();
});
