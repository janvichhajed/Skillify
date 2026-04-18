document.addEventListener('DOMContentLoaded', () => {

    // 1. Intersection Observer for staggered entrance
    const observer = new IntersectionObserver((entries) => {
        let delayCount = 0;
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('fade-in');
                    entry.target.style.opacity = '1';
                }, delayCount * 80);
                delayCount++;
                observer.unobserve(entry.target);
            }
        });
    }, { rootMargin: '0px 0px -50px 0px', threshold: 0.1 });

    const cards = document.querySelectorAll('.card-premium, .stagger-el');
    cards.forEach(card => {
        card.style.opacity = '0';
        observer.observe(card);
    });

    // 2. Button Ripple Effect
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            let x = e.clientX - e.target.getBoundingClientRect().left;
            let y = e.clientY - e.target.getBoundingClientRect().top;
            let ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // 3. Form submission loading state
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.classList.add('loading');
        });
    });

    // 4. Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if(target) target.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // 5. Active Nav Item detection
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-link, .bottom-nav a, .nav-links a');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath === href && href !== '#') {
            link.classList.add('active');
        } else if (href && currentPath.startsWith(href) && href !== '/' && href !== '#') {
            link.classList.add('active');
        }
    });

    // 6. Flash toast auto-remove
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.4s ease';
            setTimeout(() => toast.remove(), 400);
        }, 4000);
    });
});
