/**
 * News card interactivity: Favorite and Share
 * Client-side only, uses localStorage for favorites
 */

(function() {
  'use strict';

  const FAVORITES_KEY = 'acreandplate:news:favorites';

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    // Load favorites from localStorage and update UI
    loadFavorites();

    // Set up event handlers
    document.querySelectorAll('.favorite-btn').forEach(btn => {
      btn.addEventListener('click', handleFavorite);
    });

    document.querySelectorAll('.share-btn').forEach(btn => {
      btn.addEventListener('click', handleShare);
    });

    // Handle deep linking: scroll to news item if hash is present
    if (window.location.hash) {
      handleDeepLink();
    }
  }

  /**
   * Load favorites from localStorage and update button states
   */
  function loadFavorites() {
    const favorites = getFavorites();
    favorites.forEach(id => {
      const btn = document.querySelector(`.favorite-btn[data-news-id="${id}"]`);
      if (btn) {
        setFavoriteState(btn, true);
      }
    });
  }

  /**
   * Get favorites array from localStorage
   */
  function getFavorites() {
    try {
      const stored = localStorage.getItem(FAVORITES_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      console.error('Failed to load favorites:', e);
      return [];
    }
  }

  /**
   * Save favorites array to localStorage
   */
  function saveFavorites(favorites) {
    try {
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
    } catch (e) {
      console.error('Failed to save favorites:', e);
    }
  }

  /**
   * Handle favorite button click
   */
  function handleFavorite(e) {
    const btn = e.currentTarget;
    const newsId = btn.dataset.newsId;
    const favorites = getFavorites();
    const index = favorites.indexOf(newsId);
    
    if (index === -1) {
      // Add to favorites
      favorites.push(newsId);
      setFavoriteState(btn, true);
    } else {
      // Remove from favorites
      favorites.splice(index, 1);
      setFavoriteState(btn, false);
    }
    
    saveFavorites(favorites);
  }

  /**
   * Update button state (visual and aria)
   */
  function setFavoriteState(btn, isFavorited) {
    btn.setAttribute('aria-pressed', isFavorited ? 'true' : 'false');
    btn.classList.toggle('favorited', isFavorited);
    
    const label = btn.querySelector('.btn-label');
    if (label) {
      label.textContent = isFavorited ? 'Favorited' : 'Favorite';
    }
  }

  /**
   * Handle share button click
   */
  async function handleShare(e) {
    const btn = e.currentTarget;
    const title = btn.dataset.newsTitle;
    const url = btn.dataset.newsUrl;
    const text = `${title} - Acre & Plate`;

    // Try Web Share API first (mobile devices)
    if (navigator.share && navigator.canShare && navigator.canShare({ title, text, url })) {
      try {
        await navigator.share({ title, text, url });
        return;
      } catch (err) {
        // User cancelled or share failed, fall through to clipboard
        if (err.name !== 'AbortError') {
          console.error('Share failed:', err);
        }
      }
    }

    // Fallback: copy to clipboard
    try {
      await copyToClipboard(url);
      showCopyFeedback(btn);
    } catch (err) {
      console.error('Copy failed:', err);
      // Fallback for older browsers: manual selection
      fallbackCopy(url);
    }
  }

  /**
   * Copy text to clipboard using modern API
   */
  async function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
    } else {
      throw new Error('Clipboard API not available');
    }
  }

  /**
   * Fallback copy method for older browsers
   */
  function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
      document.execCommand('copy');
      const btn = document.activeElement.closest('.share-btn');
      if (btn) {
        showCopyFeedback(btn);
      }
    } catch (err) {
      console.error('Fallback copy failed:', err);
    } finally {
      document.body.removeChild(textarea);
    }
  }

  /**
   * Show "Link copied" feedback
   */
  function showCopyFeedback(btn) {
    const label = btn.querySelector('.btn-label');
    if (!label) return;
    
    const originalText = label.textContent;
    label.textContent = 'Link copied!';
    btn.classList.add('copied');
    
    setTimeout(() => {
      label.textContent = originalText;
      btn.classList.remove('copied');
    }, 2000);
  }

  /**
   * Handle deep linking: scroll to and highlight news item
   */
  function handleDeepLink() {
    const hash = window.location.hash.slice(1);
    if (!hash) return;

    const card = document.getElementById(hash);
    if (!card) return;

    // Scroll to card with some offset for header
    setTimeout(() => {
      const yOffset = -100;
      const y = card.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });

      // Add temporary highlight effect
      card.classList.add('highlighted');
      setTimeout(() => {
        card.classList.remove('highlighted');
      }, 2000);
    }, 100);
  }

})();
