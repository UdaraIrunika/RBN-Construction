/**
 * building3d.js — dependency-free CSS 3D construction model
 * R.B.N. Construction website · UIDD (Software Solutions)
 *
 * Renders a building from boxes using CSS 3D transforms and
 * "builds" it in five stages:
 *   0 Plan → 1 Foundation → 2 Structure → 3 Envelope → 4 Handover
 * Future stages are drawn as dashed blueprint outlines (ghosts).
 *
 * Usage (HTML):
 *   <div class="b3d" data-building3d data-stage="4" data-autoplay></div>
 * API:
 *   const model = Building3D.mount(el, { stage: 0 });
 *   model.setStage(2);
 */
(function () {
  'use strict';

  const STAGES = ['Plan', 'Foundation', 'Structure', 'Envelope', 'Handover'];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Model definition (units; y is up) ---------- */
  function buildModel() {
    const boxes = [];
    const add = (b) => boxes.push(Object.assign({ stage: 0, until: Infinity, temp: false }, b));
    const FLOOR = 1.7, COL_H = 1.4, BASE = 0.4, FLOORS = 3;

    // Site
    add({ m: 'ground', x: 0, y: 0, z: 0, w: 19, h: 0.02, d: 14, stage: 0 });

    // 1 — Foundation slabs
    add({ m: 'concrete', x: -1, y: 0, z: 0, w: 10, h: BASE, d: 6, stage: 1 });
    add({ m: 'concrete', x: 6, y: 0, z: 1, w: 4, h: BASE, d: 4, stage: 1 });

    // 2 — Structure: columns + slabs
    for (let f = 0; f < FLOORS; f++) {
      const y = BASE + f * FLOOR;
      [-5.7, -1, 3.7].forEach((x) => [-2.7, 2.7].forEach((z) =>
        add({ m: 'column', x, y, z, w: 0.4, h: COL_H, d: 0.4, stage: 2 })));
      add({ m: 'concrete', x: -1, y: y + COL_H, z: 0, w: 10, h: 0.3, d: 6, stage: 2 });
    }
    [4.3, 7.7].forEach((x) => [-0.7, 2.7].forEach((z) =>
      add({ m: 'column', x, y: BASE, z, w: 0.4, h: COL_H, d: 0.4, stage: 2 })));
    add({ m: 'concrete', x: 6, y: BASE + COL_H, z: 1, w: 4, h: 0.3, d: 4, stage: 2 });

    // 3 — Envelope: ground floor render, upper floors glazing, annex walls
    add({ m: 'plaster', x: -1, y: BASE, z: 0, w: 9.6, h: COL_H, d: 5.6, stage: 3 });
    for (let f = 1; f < FLOORS; f++) {
      add({ m: 'glass', x: -1, y: BASE + f * FLOOR, z: 0, w: 9.6, h: COL_H, d: 5.6, stage: 3 });
    }
    add({ m: 'plaster', x: 6, y: BASE, z: 1, w: 3.6, h: COL_H, d: 3.6, stage: 3 });

    // 4 — Handover: parapets, plant, canopy, steps, landscaping
    const top = BASE + FLOORS * FLOOR;
    add({ m: 'plaster', x: -1, y: top, z: 2.9, w: 10, h: 0.45, d: 0.2, stage: 4 });
    add({ m: 'plaster', x: -1, y: top, z: -2.9, w: 10, h: 0.45, d: 0.2, stage: 4 });
    add({ m: 'plaster', x: -5.9, y: top, z: 0, w: 0.2, h: 0.45, d: 5.6, stage: 4 });
    add({ m: 'plaster', x: 3.9, y: top, z: 0, w: 0.2, h: 0.45, d: 5.6, stage: 4 });
    add({ m: 'roof', x: -3, y: top, z: -0.8, w: 2.2, h: 0.7, d: 1.6, stage: 4 });
    add({ m: 'amber', x: -1.6, y: BASE + COL_H + 0.05, z: 3.5, w: 3.4, h: 0.16, d: 1.2, stage: 4 });
    add({ m: 'concrete', x: -1.6, y: 0, z: 3.5, w: 3, h: 0.22, d: 1, stage: 4 });
    add({ m: 'roof', x: 6, y: BASE + COL_H + 0.3, z: 1, w: 4.1, h: 0.15, d: 4.1, stage: 4 });
    [[-6.8, 4.6], [-4.6, 5.2], [3.6, 4.8], [8.2, 4.4], [8.4, -1.6]].forEach(([x, z], i) =>
      add({ m: 'tree', x, y: 0, z, w: 0.9, h: 0.9 + (i % 2) * 0.4, d: 0.9, stage: 4 }));

    // Temporary works: scaffold (structure → envelope), crane (foundation → envelope)
    add({ m: 'scaffold', x: -1, y: BASE, z: 3.35, w: 10.4, h: FLOORS * FLOOR, d: 0.5, stage: 2, until: 3, temp: true });
    add({ m: 'amber', x: -8.6, y: 0, z: -3.2, w: 0.5, h: 8.2, d: 0.5, stage: 1, until: 3, temp: true });
    add({ m: 'amber', x: -4.6, y: 8.2, z: -3.2, w: 10, h: 0.4, d: 0.45, stage: 1, until: 3, temp: true });
    add({ m: 'roof', x: -8.6, y: 7.4, z: -3.2, w: 0.9, h: 0.8, d: 0.9, stage: 1, until: 3, temp: true });
    add({ m: 'concrete', x: -10.4, y: 7.85, z: -3.2, w: 1.2, h: 0.7, d: 0.8, stage: 1, until: 3, temp: true });
    add({ m: 'roof', x: -1.2, y: 6.4, z: -3.2, w: 0.06, h: 1.8, d: 0.06, stage: 1, until: 3, temp: true });

    return boxes;
  }

  /* ---------- DOM construction ---------- */
  function face(cls, w, h, transform) {
    const el = document.createElement('div');
    el.className = 'b3d-face ' + cls;
    el.style.width = w + 'px';
    el.style.height = h + 'px';
    el.style.transform = transform;
    return el;
  }

  function renderBox(box, u) {
    const w = box.w * u, h = box.h * u, d = box.d * u;
    const el = box.el || document.createElement('div');
    el.className = 'b3d-box m-' + box.m;
    el.textContent = '';
    el.style.transform = `translate3d(${box.x * u}px, ${-box.y * u}px, ${box.z * u}px)`;
    const frag = document.createDocumentFragment();
    frag.appendChild(face('f', w, h, `translate3d(${-w / 2}px, ${-h}px, ${d / 2}px)`));
    frag.appendChild(face('f', w, h, `translate3d(${-w / 2}px, ${-h}px, ${-d / 2}px) rotateY(180deg)`));
    frag.appendChild(face('s', d, h, `translate3d(${w / 2 - d / 2}px, ${-h}px, 0) rotateY(90deg)`));
    frag.appendChild(face('s', d, h, `translate3d(${-w / 2 - d / 2}px, ${-h}px, 0) rotateY(-90deg)`));
    frag.appendChild(face('t', w, d, `translate3d(${-w / 2}px, ${-h - d / 2}px, 0) rotateX(90deg)`));
    el.appendChild(frag);
    box.el = el;
    return el;
  }

  /* ---------- Instance ---------- */
  function mount(root, opts) {
    if (!root || root.__b3d) return root && root.__b3d;
    opts = opts || {};

    const world = document.createElement('div');
    world.className = 'b3d-world';
    world.setAttribute('aria-hidden', 'true');
    root.appendChild(world);

    const label = document.createElement('div');
    label.className = 'b3d-label';
    label.setAttribute('aria-live', 'polite');
    root.appendChild(label);

    root.setAttribute('tabindex', '0');
    root.setAttribute('role', 'group');
    root.setAttribute('aria-roledescription', '3D model');
    if (!root.getAttribute('aria-label')) {
      root.setAttribute('aria-label', 'Interactive 3D building model. Drag or use the arrow keys to rotate.');
    }

    const boxes = buildModel();
    const state = {
      stage: clampStage(opts.stage != null ? opts.stage : +root.dataset.stage || 0),
      yaw: -34, baseYaw: -34, pitch: -22, targetYaw: -34, targetPitch: -22,
      dragging: false, visible: false, idle: true, t0: performance.now(), u: 0, raf: 0,
    };

    function clampStage(n) { return Math.max(0, Math.min(STAGES.length - 1, n | 0)); }

    function layout() {
      const r = root.getBoundingClientRect();
      const u = Math.max(8, Math.min(r.width / 23, r.height / 14));
      if (Math.abs(u - state.u) < 0.5) return;
      state.u = u;
      const frag = document.createDocumentFragment();
      boxes.forEach((b) => frag.appendChild(renderBox(b, u)));
      world.textContent = '';
      world.appendChild(frag);
      applyStage();
    }

    function applyStage() {
      const s = state.stage;
      boxes.forEach((b) => {
        const el = b.el;
        if (!el) return;
        if (b.temp) {
          el.classList.toggle('is-gone', s < b.stage || s > b.until);
          el.classList.remove('is-ghost');
        } else {
          el.classList.toggle('is-ghost', s < b.stage);
        }
      });
      label.innerHTML = `Stage ${s + 1} of ${STAGES.length}: <b>${STAGES[s]}</b>`;
      root.dataset.stage = String(s);
      root.dispatchEvent(new CustomEvent('b3d:stage', { detail: { stage: s, name: STAGES[s] } }));
    }

    function setStage(n) {
      const s = clampStage(n);
      if (s === state.stage && state.u) return;
      state.stage = s;
      applyStage();
    }

    function frame(now) {
      state.raf = 0;
      if (!state.dragging && state.idle && !reduceMotion) {
        const t = (now - state.t0) / 1000;
        state.targetYaw = state.baseYaw + Math.sin(t * 0.25) * 16;
      }
      state.yaw += (state.targetYaw - state.yaw) * 0.12;
      state.pitch += (state.targetPitch - state.pitch) * 0.12;
      world.style.transform = `rotateX(${state.pitch}deg) rotateY(${state.yaw}deg)`;
      const moving = Math.abs(state.targetYaw - state.yaw) > 0.05 || Math.abs(state.targetPitch - state.pitch) > 0.05;
      if (state.visible && (moving || (state.idle && !reduceMotion) || state.dragging)) {
        state.raf = requestAnimationFrame(frame);
      }
    }
    function kick() { if (!state.raf) state.raf = requestAnimationFrame(frame); }

    // Pointer rotation (horizontal drag rotates; vertical drag tilts)
    let lastX = 0, lastY = 0, idleTimer = 0;
    root.addEventListener('pointerdown', (e) => {
      if (e.target.closest('button, a')) return;
      state.dragging = true; state.idle = false;
      lastX = e.clientX; lastY = e.clientY;
      root.setPointerCapture(e.pointerId);
      clearTimeout(idleTimer);
      kick();
    });
    root.addEventListener('pointermove', (e) => {
      if (!state.dragging) return;
      state.targetYaw += (e.clientX - lastX) * 0.4;
      state.targetPitch = Math.max(-48, Math.min(-6, state.targetPitch - (e.clientY - lastY) * 0.2));
      lastX = e.clientX; lastY = e.clientY;
    });
    const endDrag = () => {
      if (!state.dragging) return;
      state.dragging = false;
      idleTimer = setTimeout(() => { state.idle = true; state.baseYaw = state.yaw; state.t0 = performance.now(); kick(); }, 4000);
    };
    root.addEventListener('pointerup', endDrag);
    root.addEventListener('pointercancel', endDrag);

    // Keyboard
    root.addEventListener('keydown', (e) => {
      const map = { ArrowLeft: [-12, 0], ArrowRight: [12, 0], ArrowUp: [0, 4], ArrowDown: [0, -4] };
      if (map[e.key]) {
        e.preventDefault();
        state.idle = false;
        state.targetYaw += map[e.key][0];
        state.targetPitch = Math.max(-48, Math.min(-6, state.targetPitch - map[e.key][1]));
        kick();
      } else if (e.key === 'PageUp' || e.key === '+') { setStage(state.stage + 1); }
      else if (e.key === 'PageDown' || e.key === '-') { setStage(state.stage - 1); }
    });

    // Visibility: animate only when on screen
    const io = new IntersectionObserver((entries) => {
      state.visible = entries[0].isIntersecting;
      if (state.visible) { layout(); kick(); }
    }, { threshold: 0.05 });
    io.observe(root);

    if ('ResizeObserver' in window) new ResizeObserver(() => layout()).observe(root);
    layout();
    world.style.transform = `rotateX(${state.pitch}deg) rotateY(${state.yaw}deg)`;

    const api = { setStage, get stage() { return state.stage; }, stages: STAGES.slice(), root };
    root.__b3d = api;
    return api;
  }

  /* ---------- Stage tabs (optional UI) ---------- */
  function bindTabs(model, container) {
    if (!container) return;
    const tabs = Array.from(container.querySelectorAll('[data-stage-tab]'));
    const sync = (s) => tabs.forEach((t) => t.setAttribute('aria-pressed', String(+t.dataset.stageTab === s)));
    tabs.forEach((t) => t.addEventListener('click', () => { container.dataset.userPicked = '1'; model.setStage(+t.dataset.stageTab); }));
    model.root.addEventListener('b3d:stage', (e) => sync(e.detail.stage));
    sync(model.stage);
  }

  /* ---------- Autoplay: build once when first seen ---------- */
  function autoplay(model, ui) {
    if (reduceMotion) { model.setStage(4); return; }
    model.setStage(0);
    const io = new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) return;
      io.disconnect();
      let s = 0;
      const step = () => {
        if (ui && ui.dataset.userPicked) return; // user took control
        s += 1;
        model.setStage(s);
        if (s < 4) setTimeout(step, 900);
      };
      setTimeout(step, 700);
    }, { threshold: 0.4 });
    io.observe(model.root);
  }

  /* ---------- Scroll-driven: steps set the stage ---------- */
  function bindScrollSteps(model, stepsRoot) {
    const steps = Array.from(stepsRoot.querySelectorAll('[data-build-step]'));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        const s = +en.target.dataset.buildStep;
        steps.forEach((st) => st.classList.toggle('is-active', st === en.target));
        model.setStage(s);
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach((s) => io.observe(s));
    if (steps[0]) steps[0].classList.add('is-active');
  }

  /* ---------- Auto-init ---------- */
  function init() {
    document.querySelectorAll('[data-building3d]').forEach((el) => {
      const model = mount(el);
      const ui = document.querySelector(`[data-b3d-ui="${el.id}"]`);
      bindTabs(model, ui);
      if (el.hasAttribute('data-autoplay')) autoplay(model, ui);
      const steps = document.querySelector(`[data-build-steps="${el.id}"]`);
      if (steps) bindScrollSteps(model, steps);
    });
  }

  window.Building3D = { mount, STAGES };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
