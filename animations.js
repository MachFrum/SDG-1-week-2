// animations.js
// Handles scroll reveal, fade-in, and interactive hover/transition effects

document.addEventListener('DOMContentLoaded', function() {
    // On-Scroll Reveal Animation
    const revealElements = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    revealElements.forEach(el => observer.observe(el));

    // Fade-in for main content
    const fadeIn = document.querySelector('.fade-in');
    if (fadeIn) {
        fadeIn.classList.add('visible');
    }

    // Button ripple effect (optional, for extra interactivity)
    document.querySelectorAll('button, .btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const circle = document.createElement('span');
            circle.className = 'ripple';
            circle.style.left = `${e.offsetX}px`;
            circle.style.top = `${e.offsetY}px`;
            this.appendChild(circle);
            setTimeout(() => circle.remove(), 600);
        });
    });
});

// Optional: Add CSS for .ripple in styles.css for a nice effect
// .ripple {
//   position: absolute;
//   border-radius: 50%;
//   transform: scale(0);
//   animation: ripple 0.6s linear;
//   background: rgba(255,255,255,0.4);
//   pointer-events: none;
//   width: 100px; height: 100px;
//   left: 50%; top: 50%;
//   z-index: 2;
// }
// @keyframes ripple {
//   to { transform: scale(2.5); opacity: 0; }
// }

// Dark mode toggle logic
const darkModeBtn = document.getElementById('darkModeToggle');
const darkVars = {
    '--bg-color': '#121212',
    '--surface-color': '#1d1d1d',
    '--primary-accent': '#9b59b6',
    '--primary-accent-darker': '#8e44ad',
    '--text-color': '#e0e0e0',
    '--text-color-muted': '#a0a0a0',
    '--border-color': '#2c2c2c',
};
const lightVars = {
    '--bg-color': '#f4f6fb',
    '--surface-color': '#fff',
    '--primary-accent': '#9b59b6',
    '--primary-accent-darker': '#8e44ad',
    '--text-color': '#22325c',
    '--text-color-muted': '#5a6b8a',
    '--border-color': '#e0e0e0',
};
function setTheme(vars) {
    for (const key in vars) {
        document.documentElement.style.setProperty(key, vars[key]);
    }
}
function enableDarkMode() {
    setTheme(darkVars);
    document.body.classList.add('dark-mode');
    if (darkModeBtn) darkModeBtn.innerText = '🌙';
    localStorage.setItem('theme', 'dark');
}
function enableLightMode() {
    setTheme(lightVars);
    document.body.classList.remove('dark-mode');
    if (darkModeBtn) darkModeBtn.innerText = '☀️';
    localStorage.setItem('theme', 'light');
}
function toggleTheme() {
    if (document.body.classList.contains('dark-mode')) {
        enableLightMode();
    } else {
        enableDarkMode();
    }
}
if (darkModeBtn) {
    darkModeBtn.addEventListener('click', toggleTheme);
    // On load, set theme from localStorage
    const saved = localStorage.getItem('theme');
    if (saved === 'light') enableLightMode();
    else enableDarkMode();
} 