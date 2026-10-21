/* Adapted from PR #109: OR within facet groups, AND across groups; URL-restorable filters. */
(() => {
  'use strict';
  const bar = document.querySelector('.filter-bar');
  if (!bar) return;
  const cards = [...document.querySelectorAll('.listings-section .listing-card')];
  const search = bar.querySelector('#filter-search');
  const state = bar.querySelector('#filter-state');
  const breed = bar.querySelector('#filter-breed');
  const chips = [...bar.querySelectorAll('.filter-chip')];
  const clear = bar.querySelector('.filter-clear');
  const empty = bar.querySelector('.filter-empty');
  const groups = ['finish', 'ships', 'pickup', 'cert', 'pet'];
  const active = Object.fromEntries(groups.map(k => [k, new Set()]));
  function restore() {
    const params = new URLSearchParams(location.search);
    search.value = params.get('q') || '';
    state.value = params.get('state') || '';
    breed.value = params.get('breed') || '';
    groups.forEach(k => { active[k] = new Set(params.getAll(k).filter(v => chips.some(c => c.dataset.filter === k && c.dataset.value === v))); });
    // Retain compatibility with the old preview's boolean query parameters.
    ['pickup', 'pet'].forEach(k => { if (params.get(k) === '1') active[k].add('true'); });
    if (groups.some(k => active[k].size)) bar.querySelector('details').open = true;
    apply(false);
  }
  function apply(updateURL = true) {
    const query = search.value.trim().toLowerCase();
    let count = 0;
    cards.forEach(card => {
      const d = card.dataset;
      const match = (!query || d.search.includes(query)) &&
        (!state.value || d.state.split('/').includes(state.value)) &&
        (!breed.value || d.breeds.split(' ').includes(breed.value)) &&
        groups.every(k => !active[k].size || (k === 'cert' ? d.certs.split('|').some(v => active[k].has(v)) : active[k].has(d[k])));
      card.hidden = !match;
      if (match) count++;
    });
    chips.forEach(chip => {
      const selected = active[chip.dataset.filter].has(chip.dataset.value);
      chip.classList.toggle('active', selected);
      chip.setAttribute('aria-pressed', String(selected));
    });
    bar.querySelector('#shown-count').textContent = count;
    clear.hidden = !(query || state.value || breed.value || groups.some(k => active[k].size));
    empty.hidden = count !== 0;
    if (updateURL) {
      const params = new URLSearchParams(location.search);
      ['q', 'state', 'breed', ...groups].forEach(k => params.delete(k));
      if (query) params.set('q', search.value.trim());
      if (state.value) params.set('state', state.value);
      if (breed.value) params.set('breed', breed.value);
      groups.forEach(k => active[k].forEach(v => params.append(k,v)));
      const suffix = params.toString();
      history.replaceState(null, '', location.pathname + (suffix ? '?' + suffix : '') + location.hash);
    }
  }
  function reset() {
    search.value = ''; state.value = ''; breed.value = '';
    groups.forEach(k => active[k].clear()); apply(); search.focus();
  }
  chips.forEach(chip => chip.addEventListener('click', () => {
    const set = active[chip.dataset.filter], value = chip.dataset.value;
    set.has(value) ? set.delete(value) : set.add(value); apply();
  }));
  search.addEventListener('input', () => apply());
  state.addEventListener('change', () => apply()); breed.addEventListener('change', () => apply());
  clear.addEventListener('click', reset); bar.querySelector('.filter-clear-inline').addEventListener('click', reset);
  window.addEventListener('popstate', restore);
  restore(); bar.hidden = false;
})();
