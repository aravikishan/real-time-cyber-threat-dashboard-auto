// Navigation Interactions
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelectorAll('nav a');

navToggle.addEventListener('click', () => {
    document.body.classList.toggle('nav-open');
});

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        document.body.classList.remove('nav-open');
    });
});

// Form Validation
const loginForm = document.querySelector('form');

if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        if (!username || !password) {
            e.preventDefault();
            alert('Please fill in all fields.');
        }
    });
}

// Smooth Scrolling
const scrollLinks = document.querySelectorAll('a[href^="#"]');

scrollLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        target.scrollIntoView({ behavior: 'smooth' });
    });
});