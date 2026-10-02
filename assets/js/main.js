/**
 * main.js — site behaviour for R.B.N. Construction
 * UIDD (Software Solutions) · vanilla JS, no dependencies
 * Modules: nav · filters · lightbox · forms · quote wizard · planner
 */
(function () {
  'use strict';

  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

  /* ---------- Mobile navigation ---------- */
  function initNav() {
    const toggle = $('.menu-toggle');
    const drawer = $('#mobile-nav');
    if (!toggle || !drawer) return;
    const setOpen = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      drawer.classList.toggle('is-open', open);
      document.body.classList.toggle('nav-open', open);
      drawer.inert = !open;
      if (open) { const first = $('a', drawer); first && first.focus(); }
    };
    drawer.inert = true;
    toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) { setOpen(false); toggle.focus(); }
    });
    window.matchMedia('(min-width: 1100px)').addEventListener('change', (e) => { if (e.matches) setOpen(false); });
  }

  /* ---------- Project filters ---------- */
  function initFilters() {
    const bar = $('[data-filters]');
    if (!bar) return;
    const cards = $$('[data-category]');
    const empty = $('[data-filter-empty]');
    const count = $('[data-filter-count]');
    const apply = (cat) => {
      let shown = 0;
      cards.forEach((c) => {
        const match = cat === 'all' || c.dataset.category.split(' ').includes(cat);
        c.hidden = !match;
        if (match) shown++;
      });
      $$('.filter-btn', bar).forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.filter === cat)));
      if (empty) empty.hidden = shown !== 0;
      if (count) count.textContent = `${shown} project${shown === 1 ? '' : 's'} shown`;
    };
    bar.addEventListener('click', (e) => {
      const btn = e.target.closest('.filter-btn');
      if (!btn) return;
      apply(btn.dataset.filter);
      history.replaceState(null, '', btn.dataset.filter === 'all' ? location.pathname : `?type=${btn.dataset.filter}`);
    });
    const initial = new URLSearchParams(location.search).get('type');
    apply(initial && $(`.filter-btn[data-filter="${CSS.escape(initial)}"]`, bar) ? initial : 'all');
  }

  /* ---------- Gallery lightbox (native <dialog>) ---------- */
  function initLightbox() {
    const dialog = $('#lightbox');
    if (!dialog || typeof dialog.showModal !== 'function') return;
    const img = $('img', dialog);
    $$('[data-lightbox]').forEach((btn) => btn.addEventListener('click', () => {
      img.src = btn.dataset.lightbox;
      img.alt = btn.querySelector('img') ? btn.querySelector('img').alt : '';
      dialog.showModal();
    }));
    $('.lightbox-close', dialog).addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });
  }

  /* ---------- Form validation ---------- */
  const MESSAGES = {
    valueMissing: 'This field is required.',
    typeMismatch: { email: 'Enter an email address like name@example.com.', url: 'Enter a full web address.' },
    patternMismatch: 'Check the format of this field.',
    tooShort: (el) => `Enter at least ${el.minLength} characters.`,
    tooLong: (el) => `Use ${el.maxLength} characters or fewer.`,
    rangeUnderflow: (el) => `Enter ${el.min} or more.`,
    rangeOverflow: (el) => `Enter ${el.max} or less.`,
  };

  function errorFor(el) {
    const v = el.validity;
    if (v.valid) return '';
    if (el.dataset.error && !v.valueMissing) return el.dataset.error;
    for (const key of Object.keys(MESSAGES)) {
      if (!v[key]) continue;
      const m = MESSAGES[key];
      if (typeof m === 'function') return m(el);
      if (typeof m === 'object') return m[el.type] || 'Check this field.';
      return m;
    }
    return 'Check this field.';
  }

  function showError(el) {
    const id = el.id + '-error';
    let msg = document.getElementById(id);
    if (!msg) {
      msg = document.createElement('p');
      msg.id = id;
      msg.className = 'field-error';
      (el.closest('.field') || el.parentNode).appendChild(msg);
    }
    const text = errorFor(el);
    msg.textContent = text;
    el.setAttribute('aria-invalid', text ? 'true' : 'false');
    const described = (el.getAttribute('aria-describedby') || '').split(' ').filter(Boolean);
    if (text && !described.includes(id)) el.setAttribute('aria-describedby', described.concat(id).join(' '));
    return !text;
  }

  function validate(scope) {
    const fields = $$('input, select, textarea', scope).filter((el) => !el.closest('.hp-field') && el.type !== 'hidden' && !el.disabled);
    let firstBad = null;
    fields.forEach((el) => { if (!showError(el) && !firstBad) firstBad = el; });
    if (firstBad) firstBad.focus();
    return !firstBad;
  }

  function liveValidate(form) {
    form.addEventListener('blur', (e) => {
      const el = e.target;
      if (el.matches('input, select, textarea') && el.value) showError(el);
    }, true);
    form.addEventListener('input', (e) => {
      if (e.target.getAttribute('aria-invalid') === 'true') showError(e.target);
    });
  }

  async function submitForm(form) {
    const status = $('.form-status', form);
    const btn = $('[type="submit"]', form);
    const setStatus = (text, ok) => {
      status.textContent = text;
      status.className = 'form-status ' + (ok ? 'is-success' : 'is-error');
      status.focus();
    };
    btn.setAttribute('aria-busy', 'true');
    btn.disabled = true;
    try {
      const data = new FormData(form);
      const res = await fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' }, credentials: 'same-origin' });
      const json = await res.json().catch(() => ({}));
      if (!res.ok || !json.ok) throw new Error(json.message || 'The message could not be sent.');
      form.reset();
      fetchToken(form);
      if ($$('.form-step', form).length) goToStep(form, 0, false);
      setStatus(form.dataset.success || 'Message sent. We will reply within one working day.', true);
    } catch (err) {
      const phone = document.body.dataset.phone || '';
      setStatus(`${err.message} Please try again, or call us on ${phone}.`, false);
    } finally {
      btn.removeAttribute('aria-busy');
      btn.disabled = false;
    }
  }

  async function fetchToken(form) {
    const input = $('input[name="csrf_token"]', form);
    if (!input || !form.dataset.tokenUrl) return;
    try {
      const res = await fetch(form.dataset.tokenUrl, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
      const json = await res.json();
      if (json.token) input.value = json.token;
    } catch (_) { /* static preview without PHP — submit will report the error */ }
  }

  function initForms() {
    $$('form[data-validate]').forEach((form) => {
      form.noValidate = true;
      liveValidate(form);
      fetchToken(form);
      const started = $('input[name="form_started"]', form);
      if (started) started.value = String(Math.floor(Date.now() / 1000));
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!validate(form)) return;
        submitForm(form);
      });
    });
  }

  /* ---------- Quote wizard (multi-step) ---------- */
  function goToStep(form, i, focus = true) {
    const steps = $$('.form-step', form);
    const nav = $$('.steps-nav li', form);
    steps.forEach((s, idx) => { s.hidden = idx !== i; });
    nav.forEach((n, idx) => {
      n.classList.toggle('is-current', idx === i);
      n.classList.toggle('is-done', idx < i);
      if (idx === i) n.setAttribute('aria-current', 'step'); else n.removeAttribute('aria-current');
    });
    form.dataset.step = String(i);
    const heading = $('h2, legend', steps[i]);
    if (heading && focus) { heading.setAttribute('tabindex', '-1'); heading.focus(); }
  }

  function initWizard() {
    const form = $('form[data-wizard]');
    if (!form) return;
    form.addEventListener('click', (e) => {
      const i = +(form.dataset.step || 0);
      if (e.target.closest('[data-next]')) {
        if (validate($$('.form-step', form)[i])) goToStep(form, i + 1);
      } else if (e.target.closest('[data-prev]')) {
        goToStep(form, Math.max(0, i - 1));
      }
    });
    // Prefill from planner (?type=&floors=&area=&finish=)
    const q = new URLSearchParams(location.search);
    const setVal = (name, val) => {
      if (!val) return;
      const radio = $(`input[name="${name}"][value="${CSS.escape(val)}"]`, form);
      if (radio) { radio.checked = true; return; }
      const el = form.elements[name];
      if (el && 'value' in el) el.value = val;
    };
    setVal('project_type', q.get('type'));
    setVal('floor_area', q.get('area'));
    setVal('floors', q.get('floors'));
    if (q.get('finish')) setVal('details', `Planner estimate: ${q.get('floors') || '?'} floor(s), ${q.get('area') || '?'} sq ft per floor, ${q.get('finish')} finish.`);
    goToStep(form, 0, false);
  }

  /* ---------- Build planner (no prices: sizes only) ---------- */
  function initPlanner() {
    const p = $('[data-planner]');
    if (!p) return;
    const out = {
      total: $('[data-out="total"]', p),
      sqm: $('[data-out="sqm"]', p),
      link: $('[data-out="link"]', p),
    };
    const calc = () => {
      const type = p.elements.type.value;
      const floors = Math.max(1, Math.min(10, +p.elements.floors.value || 1));
      const area = Math.max(0, Math.min(100000, +p.elements.area.value || 0));
      const finish = p.elements.finish.value;
      const total = floors * area;
      out.total.textContent = total ? total.toLocaleString('en-LK') + ' sq ft' : '—';
      out.sqm.textContent = total ? Math.round(total * 0.092903).toLocaleString('en-LK') + ' m²' : '—';
      const params = new URLSearchParams({ type, floors: String(floors), area: String(area), finish });
      out.link.href = 'quote.html?' + params.toString();
    };
    p.addEventListener('input', calc);
    p.addEventListener('submit', (e) => { e.preventDefault(); location.href = out.link.href; });
    calc();
  }

  /* ---------- Misc ---------- */
  function initYear() { $$('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); }); }

  function init() {
    initNav();
    initFilters();
    initLightbox();
    initForms();
    initWizard();
    initPlanner();
    initYear();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
