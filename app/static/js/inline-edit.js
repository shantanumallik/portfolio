/**
 * Inline Edit — allows logged-in admins to edit portfolio content
 * directly on the public page without leaving it.
 *
 * All changes are saved via JSON API to /admin/api/* and reflected
 * in the DOM immediately without a page reload.
 */

(function () {
  'use strict';

  // ── State ──────────────────────────────────────────────────────────────────
  let editMode = false;

  // ── Boot ───────────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', init);

  function init() {
    setupAdminBar();
    setupModal();
    setupDelegatedClicks();
  }

  // ── Admin bar ──────────────────────────────────────────────────────────────
  function setupAdminBar() {
    const toggle = document.getElementById('ie-toggle-edit');
    const editAbout = document.getElementById('ie-edit-about');
    if (toggle) toggle.addEventListener('click', toggleEditMode);
    if (editAbout) editAbout.addEventListener('click', openAboutModal);
  }

  function toggleEditMode() {
    editMode = !editMode;
    document.body.classList.toggle('ie-edit-mode', editMode);
    const btn = document.getElementById('ie-toggle-edit');
    if (btn) {
      btn.textContent = editMode ? '✓ Editing On' : '✏ Enable Editing';
      btn.classList.toggle('ie-admin-bar__btn--active', editMode);
    }
  }

  // ── Modal ──────────────────────────────────────────────────────────────────
  let currentSaveHandler = null;

  function setupModal() {
    const overlay = document.getElementById('ie-overlay');
    const closeBtn = document.getElementById('ie-modal-close');
    const cancelBtn = document.getElementById('ie-modal-cancel');
    const form = document.getElementById('ie-modal-form');

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
    if (overlay) overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeModal();
    });
    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (typeof currentSaveHandler === 'function') currentSaveHandler();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeModal();
    });
  }

  function openModal(title, fields, onSave) {
    document.getElementById('ie-modal-title').textContent = title;
    const fieldsEl = document.getElementById('ie-modal-fields');
    fieldsEl.innerHTML = '';

    fields.forEach(function (f) {
      const group = document.createElement('div');
      group.className = 'ie-field';

      const label = document.createElement('label');
      label.className = 'ie-field__label';
      label.textContent = f.label;
      label.htmlFor = 'ie-field-' + f.name;
      group.appendChild(label);

      let input;
      if (f.type === 'textarea') {
        input = document.createElement('textarea');
        input.className = 'ie-field__textarea';
        input.rows = f.rows || 5;
        input.value = f.value != null ? f.value : '';
      } else if (f.type === 'checkbox') {
        input = document.createElement('input');
        input.type = 'checkbox';
        input.className = 'ie-field__checkbox';
        input.checked = !!f.value;
      } else {
        input = document.createElement('input');
        input.type = f.type || 'text';
        input.className = 'ie-field__input';
        input.value = f.value != null ? f.value : '';
        if (f.type === 'number') { input.min = 1; input.max = 100; }
      }
      input.id = 'ie-field-' + f.name;
      input.name = f.name;
      if (f.placeholder) input.placeholder = f.placeholder;
      group.appendChild(input);

      fieldsEl.appendChild(group);
    });

    currentSaveHandler = onSave;
    const overlay = document.getElementById('ie-overlay');
    overlay.removeAttribute('aria-hidden');
    overlay.classList.add('ie-overlay--open');
    // Focus first field
    const firstInput = fieldsEl.querySelector('input, textarea');
    if (firstInput) setTimeout(function () { firstInput.focus(); }, 80);
  }

  function closeModal() {
    const overlay = document.getElementById('ie-overlay');
    overlay.classList.remove('ie-overlay--open');
    overlay.setAttribute('aria-hidden', 'true');
    currentSaveHandler = null;
  }

  function getFormData() {
    const fields = document.querySelectorAll('#ie-modal-fields [name]');
    const data = {};
    fields.forEach(function (f) {
      data[f.name] = f.type === 'checkbox' ? f.checked : f.value;
    });
    return data;
  }

  // ── API helper ─────────────────────────────────────────────────────────────
  async function api(method, url, body) {
    const opts = {
      method: method,
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
    };
    if (body !== undefined) opts.body = JSON.stringify(body);
    const res = await fetch(url, opts);
    if (!res.ok) throw new Error('Request failed: ' + res.status);
    return res.json();
  }

  // ── Delegated click handler ────────────────────────────────────────────────
  function setupDelegatedClicks() {
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      const action = btn.dataset.action;
      const id = btn.dataset.id;

      switch (action) {
        case 'edit-exp':     openEditExp(id, btn.closest('[data-exp-id]'));     break;
        case 'delete-exp':   confirmDeleteExp(id, btn.closest('[data-exp-id]')); break;
        case 'add-exp':      openAddExp();                                        break;
        case 'edit-project': openEditProject(id, btn.closest('[data-project-id]')); break;
        case 'delete-project': confirmDeleteProject(id, btn.closest('[data-project-id]')); break;
        case 'add-project':  openAddProject();                                    break;
        case 'edit-skill':   openEditSkill(id, btn.closest('[data-skill-id]'));   break;
        case 'delete-skill': confirmDeleteSkill(id, btn.closest('[data-skill-id]')); break;
        case 'add-skill':    openAddSkill();                                       break;
      }
    });
  }

  // ── EXPERIENCE ─────────────────────────────────────────────────────────────
  function expFields(d) {
    return [
      { name: 'company',      label: 'Company',                          value: d.company || '' },
      { name: 'role',         label: 'Role / Title',                     value: d.role || '' },
      { name: 'start_date',   label: 'Start Date (e.g. Jan 2025)',       value: d.start_date || '' },
      { name: 'end_date',     label: 'End Date (or "Present")',          value: d.end_date || 'Present' },
      { name: 'description',  label: 'Description', type: 'textarea', rows: 7, value: d.description || '' },
      { name: 'technologies', label: 'Technologies (comma-separated)',   value: d.technologies || '' },
      { name: 'order',        label: 'Display Order (0 = first)', type: 'number', value: d.order != null ? d.order : 0 },
    ];
  }

  function openEditExp(id, cardEl) {
    api('GET', '/admin/api/experience/' + id).then(function (d) {
      openModal('Edit Experience — ' + d.company, expFields(d), async function () {
        try {
          const result = await api('PUT', '/admin/api/experience/' + id, getFormData());
          if (result.ok) { updateExpCard(cardEl, result.data); closeModal(); }
        } catch (err) { alert('Save failed: ' + err.message); }
      });
    });
  }

  function openAddExp() {
    openModal('Add Experience', expFields({}), async function () {
      try {
        const result = await api('POST', '/admin/api/experience', getFormData());
        if (result.ok) {
          const el = buildExpCard(result.data);
          const addRow = document.getElementById('ie-add-exp-row');
          addRow ? addRow.before(el) : document.querySelector('.timeline').appendChild(el);
          triggerReveal(el);
          closeModal();
        }
      } catch (err) { alert('Save failed: ' + err.message); }
    });
  }

  function confirmDeleteExp(id, cardEl) {
    if (!confirm('Delete this experience entry?')) return;
    api('DELETE', '/admin/api/experience/' + id).then(function (r) {
      if (r.ok) cardEl.remove();
    }).catch(function (err) { alert('Delete failed: ' + err.message); });
  }

  function updateExpCard(cardEl, d) {
    cardEl.dataset.expId = d.id;
    qs(cardEl, '.timeline__company').textContent = d.company;
    qs(cardEl, '.timeline__role').textContent = d.role;
    qs(cardEl, '.timeline__period').textContent = d.start_date + ' — ' + d.end_date;
    qs(cardEl, '.timeline__desc').textContent = d.description;
    const tagsEl = cardEl.querySelector('.timeline__tags');
    if (tagsEl) tagsEl.innerHTML = techTags(d.technologies, 'tag tag--sm');
    else if (d.technologies) {
      const div = document.createElement('div');
      div.className = 'timeline__tags';
      div.innerHTML = techTags(d.technologies, 'tag tag--sm');
      cardEl.querySelector('.timeline__card').appendChild(div);
    }
  }

  function buildExpCard(d) {
    const wrap = document.createElement('div');
    wrap.className = 'timeline__item reveal';
    wrap.dataset.expId = d.id;
    wrap.innerHTML =
      '<div class="ie-card-controls">' +
        '<button class="ie-card-btn ie-card-btn--edit" data-action="edit-exp" data-id="' + d.id + '">✏</button>' +
        '<button class="ie-card-btn ie-card-btn--delete" data-action="delete-exp" data-id="' + d.id + '">✕</button>' +
      '</div>' +
      '<div class="timeline__dot"></div>' +
      '<div class="timeline__card">' +
        '<div class="timeline__meta">' +
          '<span class="timeline__company">' + esc(d.company) + '</span>' +
          '<span class="timeline__period">' + esc(d.start_date) + ' — ' + esc(d.end_date) + '</span>' +
        '</div>' +
        '<h3 class="timeline__role">' + esc(d.role) + '</h3>' +
        '<p class="timeline__desc">' + esc(d.description) + '</p>' +
        (d.technologies ? '<div class="timeline__tags">' + techTags(d.technologies, 'tag tag--sm') + '</div>' : '') +
      '</div>';
    return wrap;
  }

  // ── PROJECTS ───────────────────────────────────────────────────────────────
  function projectFields(d) {
    return [
      { name: 'title',       label: 'Title',                      value: d.title || '' },
      { name: 'tagline',     label: 'Tagline (short summary)',    value: d.tagline || '' },
      { name: 'description', label: 'Description', type: 'textarea', rows: 6, value: d.description || '' },
      { name: 'tech_stack',  label: 'Tech Stack (comma-separated)', value: d.tech_stack || '' },
      { name: 'github_url',  label: 'GitHub URL',                 value: d.github_url || '' },
      { name: 'demo_url',    label: 'Live Demo URL',              value: d.demo_url || '' },
      { name: 'image_url',   label: 'Image URL (optional)',       value: d.image_url || '' },
      { name: 'is_featured', label: 'Featured project?', type: 'checkbox', value: d.is_featured || false },
      { name: 'order',       label: 'Display Order (0 = first)', type: 'number', value: d.order != null ? d.order : 0 },
    ];
  }

  function openEditProject(id, cardEl) {
    api('GET', '/admin/api/projects/' + id).then(function (d) {
      openModal('Edit Project — ' + d.title, projectFields(d), async function () {
        try {
          const result = await api('PUT', '/admin/api/projects/' + id, getFormData());
          if (result.ok) { updateProjectCard(cardEl, result.data); closeModal(); }
        } catch (err) { alert('Save failed: ' + err.message); }
      });
    });
  }

  function openAddProject() {
    openModal('Add Project', projectFields({}), async function () {
      try {
        const result = await api('POST', '/admin/api/projects', getFormData());
        if (result.ok) {
          const el = buildProjectCard(result.data);
          const grid = document.querySelector('.projects-grid');
          const addRow = document.getElementById('ie-add-project-row');
          if (grid) grid.appendChild(el);
          else if (addRow) addRow.before(el);
          triggerReveal(el);
          closeModal();
        }
      } catch (err) { alert('Save failed: ' + err.message); }
    });
  }

  function confirmDeleteProject(id, cardEl) {
    if (!confirm('Delete this project?')) return;
    api('DELETE', '/admin/api/projects/' + id).then(function (r) {
      if (r.ok) cardEl.remove();
    }).catch(function (err) { alert('Delete failed: ' + err.message); });
  }

  function updateProjectCard(cardEl, d) {
    cardEl.dataset.projectId = d.id;
    const titleEl = qs(cardEl, '.project-card__title');
    if (titleEl) titleEl.textContent = d.title;
    const taglineEl = cardEl.querySelector('.project-card__tagline');
    if (taglineEl) taglineEl.textContent = d.tagline;
    const descEl = qs(cardEl, '.project-card__desc');
    if (descEl) descEl.textContent = d.description;
    const tagsEl = cardEl.querySelector('.project-card__tags');
    if (tagsEl) tagsEl.innerHTML = techTags(d.tech_stack, 'tag');
    const badge = cardEl.querySelector('.badge');
    if (d.is_featured && !badge) {
      const b = document.createElement('span');
      b.className = 'badge'; b.textContent = 'Featured';
      qs(cardEl, '.project-card__body').prepend(b);
    } else if (!d.is_featured && badge) {
      badge.remove();
    }
    // Links
    updateCardLinks(cardEl, d);
  }

  function updateCardLinks(cardEl, d) {
    const linksEl = cardEl.querySelector('.project-card__links');
    if (!linksEl) return;
    linksEl.innerHTML = '';
    if (d.github_url) {
      const a = document.createElement('a');
      a.href = d.github_url; a.target = '_blank'; a.rel = 'noopener';
      a.className = 'btn btn--ghost btn--sm'; a.textContent = 'GitHub ↗';
      linksEl.appendChild(a);
    }
    if (d.demo_url) {
      const a = document.createElement('a');
      a.href = d.demo_url; a.target = '_blank'; a.rel = 'noopener';
      a.className = 'btn btn--primary btn--sm'; a.textContent = 'Live Demo ↗';
      linksEl.appendChild(a);
    }
  }

  function buildProjectCard(d) {
    const el = document.createElement('article');
    el.className = 'project-card reveal';
    el.dataset.projectId = d.id;
    el.innerHTML =
      '<div class="ie-card-controls">' +
        '<button class="ie-card-btn ie-card-btn--edit" data-action="edit-project" data-id="' + d.id + '">✏</button>' +
        '<button class="ie-card-btn ie-card-btn--delete" data-action="delete-project" data-id="' + d.id + '">✕</button>' +
      '</div>' +
      '<div class="project-card__image project-card__image--placeholder">' +
        '<div class="project-card__placeholder-icon">💻</div>' +
      '</div>' +
      '<div class="project-card__body">' +
        (d.is_featured ? '<span class="badge">Featured</span>' : '') +
        '<h3 class="project-card__title">' + esc(d.title) + '</h3>' +
        (d.tagline ? '<p class="project-card__tagline">' + esc(d.tagline) + '</p>' : '') +
        '<p class="project-card__desc">' + esc(d.description) + '</p>' +
        (d.tech_stack ? '<div class="project-card__tags">' + techTags(d.tech_stack, 'tag') + '</div>' : '') +
        '<div class="project-card__links">' +
          (d.github_url ? '<a href="' + esc(d.github_url) + '" target="_blank" rel="noopener" class="btn btn--ghost btn--sm">GitHub ↗</a>' : '') +
          (d.demo_url ? '<a href="' + esc(d.demo_url) + '" target="_blank" rel="noopener" class="btn btn--primary btn--sm">Live Demo ↗</a>' : '') +
        '</div>' +
      '</div>';
    return el;
  }

  // ── SKILLS ─────────────────────────────────────────────────────────────────
  function skillFields(d) {
    return [
      { name: 'name',        label: 'Skill Name',                       value: d.name || '' },
      { name: 'category',    label: 'Category (e.g. Agentic AI)',       value: d.category || '' },
      { name: 'proficiency', label: 'Proficiency (1–100)', type: 'number', value: d.proficiency != null ? d.proficiency : 80 },
      { name: 'is_featured', label: 'Featured?', type: 'checkbox',      value: d.is_featured || false },
      { name: 'order',       label: 'Display Order (0 = first)', type: 'number', value: d.order != null ? d.order : 0 },
    ];
  }

  function openEditSkill(id, cardEl) {
    api('GET', '/admin/api/skills/' + id).then(function (d) {
      openModal('Edit Skill — ' + d.name, skillFields(d), async function () {
        try {
          const result = await api('PUT', '/admin/api/skills/' + id, getFormData());
          if (result.ok) { updateSkillCard(cardEl, result.data); closeModal(); }
        } catch (err) { alert('Save failed: ' + err.message); }
      });
    });
  }

  function openAddSkill() {
    openModal('Add Skill', skillFields({}), async function () {
      try {
        const result = await api('POST', '/admin/api/skills', getFormData());
        if (result.ok) {
          const el = buildSkillCard(result.data);
          // Try to find the matching category group, or append to last group
          const groups = document.querySelectorAll('.skill-group');
          let targetGrid = null;
          groups.forEach(function (g) {
            if (g.querySelector('.skill-group__title') &&
                g.querySelector('.skill-group__title').textContent.trim().toLowerCase() ===
                (result.data.category || '').toLowerCase()) {
              targetGrid = g.querySelector('.skill-grid');
            }
          });
          if (!targetGrid && groups.length) {
            targetGrid = groups[groups.length - 1].querySelector('.skill-grid');
          }
          if (targetGrid) targetGrid.appendChild(el);
          triggerReveal(el);
          closeModal();
        }
      } catch (err) { alert('Save failed: ' + err.message); }
    });
  }

  function confirmDeleteSkill(id, cardEl) {
    if (!confirm('Delete this skill?')) return;
    api('DELETE', '/admin/api/skills/' + id).then(function (r) {
      if (r.ok) cardEl.remove();
    }).catch(function (err) { alert('Delete failed: ' + err.message); });
  }

  function updateSkillCard(cardEl, d) {
    cardEl.dataset.skillId = d.id;
    const nameEl = cardEl.querySelector('.skill-card__name');
    const pctEl = cardEl.querySelector('.skill-card__pct');
    const barEl = cardEl.querySelector('.skill-bar__fill');
    if (nameEl) nameEl.textContent = d.name;
    if (pctEl) pctEl.textContent = d.proficiency + '%';
    if (barEl) { barEl.style.width = d.proficiency + '%'; barEl.dataset.width = d.proficiency; }
  }

  function buildSkillCard(d) {
    const el = document.createElement('div');
    el.className = 'skill-card';
    el.dataset.skillId = d.id;
    el.innerHTML =
      '<div class="ie-card-controls ie-card-controls--skill">' +
        '<button class="ie-card-btn ie-card-btn--edit" data-action="edit-skill" data-id="' + d.id + '">✏</button>' +
        '<button class="ie-card-btn ie-card-btn--delete" data-action="delete-skill" data-id="' + d.id + '">✕</button>' +
      '</div>' +
      '<div class="skill-card__header">' +
        '<span class="skill-card__name">' + esc(d.name) + '</span>' +
        '<span class="skill-card__pct">' + d.proficiency + '%</span>' +
      '</div>' +
      '<div class="skill-bar"><div class="skill-bar__fill" data-width="' + d.proficiency + '" style="width:' + d.proficiency + '%"></div></div>';
    return el;
  }

  // ── ABOUT ──────────────────────────────────────────────────────────────────
  function openAboutModal() {
    api('GET', '/admin/api/about').then(function (d) {
      openModal('Edit About & Hero', [
        { name: 'hero_tagline',  label: 'Hero Tagline (large headline)',   value: d.hero_tagline },
        { name: 'hero_subtitle', label: 'Hero Subtitle (below tagline)',   value: d.hero_subtitle },
        { name: 'bio',           label: 'Bio Paragraph', type: 'textarea', rows: 6, value: d.bio },
        { name: 'location',      label: 'Location',                        value: d.location },
        { name: 'email',         label: 'Email',                           value: d.email },
        { name: 'linkedin_url',  label: 'LinkedIn URL',                    value: d.linkedin_url },
        { name: 'github_url',    label: 'GitHub URL',                      value: d.github_url },
        { name: 'resume_url',    label: 'Resume / CV URL',                 value: d.resume_url },
      ], async function () {
        try {
          const result = await api('PUT', '/admin/api/about', getFormData());
          if (result.ok) {
            updateAboutSection(result.data);
            closeModal();
          }
        } catch (err) { alert('Save failed: ' + err.message); }
      });
    });
  }

  function updateAboutSection(d) {
    const tagline = document.querySelector('.hero__title');
    const subtitle = document.querySelector('.hero__subtitle');
    const bioEl = document.querySelector('.about__bio p');
    const emailEl = document.querySelector('.contact__email');
    const locEl = document.querySelector('.contact__location');
    if (tagline) tagline.childNodes.forEach(function (n) {
      if (n.nodeType === 3) n.textContent = ' ' + d.hero_tagline + ' ';
    });
    if (subtitle) subtitle.textContent = d.hero_subtitle;
    if (bioEl) bioEl.textContent = d.bio;
    if (emailEl && d.email) { emailEl.textContent = d.email; emailEl.href = 'mailto:' + d.email; }
    if (locEl && d.location) locEl.textContent = '📍 ' + d.location;
  }

  // ── Utilities ──────────────────────────────────────────────────────────────
  function esc(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function qs(parent, selector) {
    return parent.querySelector(selector);
  }

  function techTags(techStr, cls) {
    if (!techStr) return '';
    return techStr.split(',').map(function (t) {
      return '<span class="' + cls + '">' + esc(t.trim()) + '</span>';
    }).join('');
  }

  function triggerReveal(el) {
    setTimeout(function () { el.classList.add('visible'); }, 50);
  }

}());
