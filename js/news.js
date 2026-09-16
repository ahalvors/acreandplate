/**
 * Acre & Plate - News functionality
 * Handles Favorite and Share actions for news stories
 */

(function() {
    'use strict';
    
    // Initialize favorites from localStorage
    const FAVORITES_KEY = 'acreandplate_news_favorites';
    
    function getFavorites() {
        try {
            const stored = localStorage.getItem(FAVORITES_KEY);
            return stored ? JSON.parse(stored) : [];
        } catch (e) {
            return [];
        }
    }
    
    function saveFavorites(favorites) {
        try {
            localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
        } catch (e) {
            console.error('Failed to save favorites', e);
        }
    }
    
    function toggleFavorite(itemId) {
        const favorites = getFavorites();
        const index = favorites.indexOf(itemId);
        
        if (index > -1) {
            favorites.splice(index, 1);
        } else {
            favorites.push(itemId);
        }
        
        saveFavorites(favorites);
        return favorites.includes(itemId);
    }
    
    function isFavorited(itemId) {
        return getFavorites().includes(itemId);
    }
    
    // Initialize favorite buttons
    function initFavorites() {
        const favoriteButtons = document.querySelectorAll('.news-favorite');
        
        favoriteButtons.forEach(button => {
            const itemId = button.dataset.id;
            
            // Set initial state
            if (isFavorited(itemId)) {
                button.classList.add('is-favorited');
            }
            
            // Handle clicks
            button.addEventListener('click', function() {
                const isFav = toggleFavorite(itemId);
                button.classList.toggle('is-favorited', isFav);
                
                // Optional: visual feedback
                button.style.transform = 'scale(1.3)';
                setTimeout(() => {
                    button.style.transform = '';
                }, 200);
            });
        });
    }
    
    // Initialize share buttons
    function initShare() {
        const shareButtons = document.querySelectorAll('.news-share');
        
        shareButtons.forEach(button => {
            button.addEventListener('click', async function() {
                const url = button.dataset.url;
                const title = button.dataset.title;
                
                // Use Web Share API if available
                if (navigator.share) {
                    try {
                        await navigator.share({
                            title: title,
                            url: url
                        });
                    } catch (err) {
                        // User cancelled or error occurred
                        if (err.name !== 'AbortError') {
                            fallbackShare(url);
                        }
                    }
                } else {
                    fallbackShare(url);
                }
            });
        });
    }
    
    // Fallback: copy to clipboard
    function fallbackShare(url) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(url).then(() => {
                showNotification('Link copied to clipboard!');
            }).catch(() => {
                showNotification('Failed to copy link');
            });
        } else {
            showNotification('Copy this link: ' + url);
        }
    }
    
    // Simple notification
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'news-notification';
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 2500);
    }
    
    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initFavorites();
            initShare();
        });
    } else {
        initFavorites();
        initShare();
    }
})();
