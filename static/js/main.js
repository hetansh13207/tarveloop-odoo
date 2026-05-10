/* Traveloop — main.js */

// ── THEME TOGGLE ──
const html = document.documentElement;
const THEME_KEY = 'traveloop-theme';

function getTheme() { return localStorage.getItem(THEME_KEY) || 'dark'; }
function setTheme(t) {
    html.setAttribute('data-theme', t);
    localStorage.setItem(THEME_KEY, t);
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.innerHTML = t === 'dark' ? iconSun() : iconMoon();
}
function toggleTheme() { setTheme(getTheme() === 'dark' ? 'light' : 'dark'); }

function iconSun() {
    return `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/>
        <line x1="12" y1="21" x2="12" y2="23"/>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
        <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </svg>`;
}
function iconMoon() {
    return `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
    </svg>`;
}

// ── MOBILE MENU ──
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (menu) menu.classList.toggle('open');
}

// ── AUTO-DISMISS FLASH MESSAGES ──
function initFlash() {
    document.querySelectorAll('.flash-msg').forEach(el => {
        setTimeout(() => {
            el.style.transition = 'opacity 0.4s, transform 0.4s';
            el.style.opacity = '0';
            el.style.transform = 'translateY(-8px)';
            setTimeout(() => el.remove(), 400);
        }, 6000);
    });
}

// ── PARALLAX HERO IMAGE ──
function initParallax() {
    const heroBg = document.querySelector('.hero-img-bg');
    if (!heroBg) return;
    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;
        heroBg.style.transform = `scale(1.06) translateY(${scrolled * 0.12}px)`;
    }, { passive: true });
}

// ── STAGGERED FADE-UP ──
function initStaggeredFade() {
    const cards = document.querySelectorAll('.trip-img-card, .city-card, .dest-card, .stat-card');
    cards.forEach((card, i) => {
        card.style.animationDelay = `${i * 0.07}s`;
    });
}

// ── CUSTOM FILE INPUT LABEL ──
function initFileInput() {
    const input = document.getElementById('profile-photo-input');
    const label = document.getElementById('file-label-text');
    if (input && label) {
        input.addEventListener('change', () => {
            label.textContent = input.files.length > 0 ? input.files[0].name : 'No file chosen';
        });
    }
}

// ── INIT ──
document.addEventListener('DOMContentLoaded', () => {
    setTheme(getTheme());
    initFlash();
    initParallax();
    initStaggeredFade();
    initFileInput();

    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    const hambBtn = document.getElementById('hamburger-btn');
    if (hambBtn) hambBtn.addEventListener('click', toggleMobileMenu);
});
