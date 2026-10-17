/**
 * Client-side listing filters for Acre & Plate
 * Works without JS (all cards visible), enhances with filtering when available
 */

(function() {
    'use strict';
    
    // Check if we're on a page with filters
    const filterBar = document.querySelector('.filter-bar');
    if (!filterBar) return;
    
    const cards = document.querySelectorAll('.listing-card');
    const filterPanel = filterBar.querySelector('.filter-panel');
    const filterToggle = filterBar.querySelector('.filter-toggle');
    const filterClear = filterBar.querySelector('.filter-clear');
    const filterClearInline = filterBar.querySelector('.filter-clear-inline');
    const filterSearch = document.getElementById('filter-search');
    const shownCount = document.getElementById('shown-count');
    const totalCount = document.getElementById('total-count');
    const filterEmpty = filterBar.querySelector('.filter-empty');
    
    // Active filters state
    const activeFilters = {
        finish: new Set(),
        ships: new Set(),
        pickup: new Set(),
        cert: new Set(),
        pet: new Set(),
        search: ''
    };
    
    // Parse URL query params on load
    function parseURLFilters() {
        const params = new URLSearchParams(window.location.search);
        
        // Parse multi-value params
        const finish = params.getAll('finish');
        const ships = params.getAll('ships');
        const cert = params.getAll('cert');
        
        if (finish.length) activeFilters.finish = new Set(finish);
        if (ships.length) activeFilters.ships = new Set(ships);
        if (cert.length) activeFilters.cert = new Set(cert);
        
        // Parse single-value params
        if (params.get('pickup')) activeFilters.pickup.add('true');
        if (params.get('pet')) activeFilters.pet.add('true');
        if (params.get('q')) activeFilters.search = params.get('q');
    }
    
    // Update URL with current filters
    function updateURL() {
        const params = new URLSearchParams();
        
        activeFilters.finish.forEach(v => params.append('finish', v));
        activeFilters.ships.forEach(v => params.append('ships', v));
        activeFilters.cert.forEach(v => params.append('cert', v));
        if (activeFilters.pickup.size) params.set('pickup', '1');
        if (activeFilters.pet.size) params.set('pet', '1');
        if (activeFilters.search) params.set('q', activeFilters.search);
        
        const newURL = params.toString() 
            ? `${window.location.pathname}?${params.toString()}`
            : window.location.pathname;
        
        window.history.replaceState({}, '', newURL);
    }
    
    // Check if a card matches current filters
    function cardMatches(card) {
        // Search filter (name, city, breeds) - AND with other filters
        if (activeFilters.search) {
            const query = activeFilters.search.toLowerCase();
            const name = card.dataset.name || '';
            const city = card.dataset.city || '';
            const breeds = card.dataset.breeds || '';
            const searchText = `${name} ${city} ${breeds}`;
            if (!searchText.includes(query)) return false;
        }
        
        // Finish filter - OR within group
        if (activeFilters.finish.size > 0) {
            const cardFinish = card.dataset.finish;
            if (!cardFinish || !activeFilters.finish.has(cardFinish)) return false;
        }
        
        // Shipping filter - OR within group
        if (activeFilters.ships.size > 0) {
            const cardShips = card.dataset.ships;
            if (!cardShips || !activeFilters.ships.has(cardShips)) return false;
        }
        
        // Pickup filter
        if (activeFilters.pickup.size > 0) {
            if (!card.dataset.pickup) return false;
        }
        
        // Cert filter - OR within group (match any cert)
        if (activeFilters.cert.size > 0) {
            const cardCerts = card.dataset.certs ? card.dataset.certs.split('|') : [];
            const hasMatch = cardCerts.some(c => activeFilters.cert.has(c));
            if (!hasMatch) return false;
        }
        
        // Pet filter
        if (activeFilters.pet.size > 0) {
            if (!card.dataset.pet) return false;
        }
        
        return true;
    }
    
    // Update card visibility and counts
    function applyFilters() {
        let visibleCount = 0;
        
        cards.forEach(card => {
            if (cardMatches(card)) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Update count
        shownCount.textContent = visibleCount;
        
        // Show/hide clear button
        const hasActiveFilters = 
            activeFilters.finish.size > 0 ||
            activeFilters.ships.size > 0 ||
            activeFilters.pickup.size > 0 ||
            activeFilters.cert.size > 0 ||
            activeFilters.pet.size > 0 ||
            activeFilters.search !== '';
        
        if (hasActiveFilters) {
            filterClear.style.display = '';
        } else {
            filterClear.style.display = 'none';
        }
        
        // Show/hide empty state
        if (visibleCount === 0 && hasActiveFilters) {
            filterEmpty.style.display = 'block';
        } else {
            filterEmpty.style.display = 'none';
        }
        
        updateURL();
    }
    
    // Toggle a filter chip
    function toggleChip(chip) {
        const filterType = chip.dataset.filter;
        const filterValue = chip.dataset.value;
        
        if (chip.classList.contains('active')) {
            chip.classList.remove('active');
            activeFilters[filterType].delete(filterValue);
        } else {
            chip.classList.add('active');
            activeFilters[filterType].add(filterValue);
        }
        
        applyFilters();
    }
    
    // Clear all filters
    function clearAllFilters() {
        // Reset state
        activeFilters.finish.clear();
        activeFilters.ships.clear();
        activeFilters.pickup.clear();
        activeFilters.cert.clear();
        activeFilters.pet.clear();
        activeFilters.search = '';
        
        // Reset UI
        document.querySelectorAll('.filter-chip.active').forEach(chip => {
            chip.classList.remove('active');
        });
        
        if (filterSearch) {
            filterSearch.value = '';
        }
        
        applyFilters();
    }
    
    // Mobile toggle
    if (filterToggle) {
        filterToggle.addEventListener('click', () => {
            const isExpanded = filterToggle.getAttribute('aria-expanded') === 'true';
            filterToggle.setAttribute('aria-expanded', !isExpanded);
            filterPanel.classList.toggle('open');
        });
    }
    
    // Chip clicks
    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', () => toggleChip(chip));
    });
    
    // Clear buttons
    if (filterClear) {
        filterClear.addEventListener('click', clearAllFilters);
    }
    if (filterClearInline) {
        filterClearInline.addEventListener('click', clearAllFilters);
    }
    
    // Search input
    if (filterSearch) {
        filterSearch.addEventListener('input', (e) => {
            activeFilters.search = e.target.value.toLowerCase();
            applyFilters();
        });
    }
    
    // Initialize from URL on load
    parseURLFilters();
    
    // Set initial chip states from URL
    document.querySelectorAll('.filter-chip').forEach(chip => {
        const filterType = chip.dataset.filter;
        const filterValue = chip.dataset.value;
        if (activeFilters[filterType].has(filterValue)) {
            chip.classList.add('active');
        }
    });
    
    // Set initial search value
    if (filterSearch && activeFilters.search) {
        filterSearch.value = activeFilters.search;
    }
    
    // Apply initial filters
    applyFilters();
})();
