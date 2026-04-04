/* ============================================================
   PORTFOLIO — Public JS (Canvas Particles + Animations)
   ============================================================ */

/* ── Particle Canvas ──────────────────────────────────────── */
(function initCanvas() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const COLORS = ['#5e9bff', '#a78bfa', '#34d399', '#ffffff'];
  const PARTICLE_COUNT = 90;
  const particles = [];

  function resize() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  }

  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.r = Math.random() * 1.6 + 0.3;
      this.vx = (Math.random() - 0.5) * 0.35;
      this.vy = (Math.random() - 0.5) * 0.35;
      this.alpha = Math.random() * 0.55 + 0.08;
      this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      if (this.x < -10 || this.x > canvas.width + 10 ||
          this.y < -10 || this.y > canvas.height + 10) this.reset();
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.globalAlpha = this.alpha;
      ctx.fill();
      ctx.globalAlpha = 1;
    }
  }

  function drawConnections() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = '#5e9bff';
          ctx.globalAlpha = (1 - dist / 120) * 0.08;
          ctx.lineWidth = 0.5;
          ctx.stroke();
          ctx.globalAlpha = 1;
        }
      }
    }
  }

  for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());

  function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawConnections();
    particles.forEach(p => { p.update(); p.draw(); });
    requestAnimationFrame(loop);
  }

  resize();
  window.addEventListener('resize', resize);
  loop();
})();

/* ── Nav Scroll Effect ────────────────────────────────────── */
(function initNav() {
  const nav = document.getElementById('main-nav');
  const hamburger = document.getElementById('nav-hamburger');
  const links = document.querySelector('.nav__links');
  if (!nav) return;

  window.addEventListener('scroll', () => {
    nav.classList.toggle('nav--scrolled', window.scrollY > 40);
  }, { passive: true });

  hamburger && hamburger.addEventListener('click', () => {
    links.classList.toggle('open');
  });

  // Close menu on link click
  links && links.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => links.classList.remove('open'));
  });
})();

/* ── Reveal on Scroll ─────────────────────────────────────── */
(function initReveal() {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const delay = parseFloat(entry.target.dataset.delay || 0) * 1000;
        setTimeout(() => entry.target.classList.add('visible'), delay);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  // Immediately reveal elements already visible in the viewport,
  // observe the rest for scroll-triggered reveal.
  els.forEach((el, i) => {
    const rect = el.getBoundingClientRect();
    const inView = rect.top < window.innerHeight && rect.bottom > 0;
    if (inView) {
      // Stagger hero elements slightly for a cinematic entrance
      setTimeout(() => el.classList.add('visible'), i * 80);
    } else {
      observer.observe(el);
    }
  });

  // Safety fallback: force all elements visible after 2.5 s
  // in case observer never fires (e.g. browser quirks)
  setTimeout(() => {
    document.querySelectorAll('.reveal:not(.visible)').forEach(el => {
      el.classList.add('visible');
    });
  }, 2500);
})();

/* ── Skill Bar Animations ─────────────────────────────────── */
(function initSkillBars() {
  const bars = document.querySelectorAll('.skill-bar__fill');
  if (!bars.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        bar.style.width = bar.dataset.width + '%';
        observer.unobserve(bar);
      }
    });
  }, { threshold: 0.3 });

  bars.forEach(b => observer.observe(b));
})();

/* ── Flash auto-dismiss ───────────────────────────────────── */
(function initFlash() {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(f => {
    setTimeout(() => {
      f.style.transition = 'opacity 0.5s';
      f.style.opacity = '0';
      setTimeout(() => f.remove(), 500);
    }, 4000);
  });
})();

/* ── Back to top ──────────────────────────────────────────── */
(function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
})();
