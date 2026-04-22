document.addEventListener('DOMContentLoaded', () => {

    // 1. Page entrance stagger animation with IntersectionObserver
    const observer = new IntersectionObserver((entries) => {
        let delayCount = 0;
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.animation = `slideUpFade 0.4s ease forwards`;
                }, delayCount * 60);
                delayCount++;
                observer.unobserve(entry.target);
            }
        });
    }, { rootMargin: '0px 0px -20px 0px', threshold: 0.1 });

    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(el => {
        observer.observe(el);
    });

    // 2. Ripple effect on buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            let rect = e.target.getBoundingClientRect();
            let x = e.clientX - rect.left;
            let y = e.clientY - rect.top;
            let ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            // Only append if it's the actual button, not an inner span/icon
            if (e.target === this || this.contains(e.target)) {
               this.appendChild(ripple);
            }
            setTimeout(() => {
                if(ripple.parentNode) ripple.parentNode.removeChild(ripple);
            }, 600);
        });
    });

    // 3. Form submit loading state
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Save original width to prevent shifting
                submitBtn.style.width = submitBtn.offsetWidth + 'px';
                submitBtn.innerHTML = `<svg class="spinner" viewBox="0 0 50 50" style="width: 16px; height: 16px; margin-right: 8px; animation: rotate 2s linear infinite;"><circle cx="25" cy="25" r="20" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" style="stroke-dasharray: 1, 200; stroke-dashoffset: 0; animation: dash 1.5s ease-in-out infinite;"></circle></svg> Loading...`;
                submitBtn.style.pointerEvents = 'none';
            }
        });
    });

    // Add spinner keyframes dynamically if not present
    if (!document.getElementById('spinner-styles')) {
        const style = document.createElement('style');
        style.id = 'spinner-styles';
        style.innerHTML = `
            @keyframes rotate { 100% { transform: rotate(360deg); } }
            @keyframes dash { 
                0% { stroke-dasharray: 1, 200; stroke-dashoffset: 0; }
                50% { stroke-dasharray: 89, 200; stroke-dashoffset: -35px; }
                100% { stroke-dasharray: 89, 200; stroke-dashoffset: -124px; }
            }
        `;
        document.head.appendChild(style);
    }

    // 4. Sidebar active route auto-select
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-link, .bottom-nav a');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath === href) {
            link.classList.add('active');
        } else if (href && href !== '/' && currentPath.startsWith(href)) {
            link.classList.add('active');
        }
    });

    // 5. Flash messages disappearance
    const flashList = document.querySelectorAll('.flash-msg');
    flashList.forEach((msg, idx) => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            msg.style.transition = 'all 0.3s ease';
            setTimeout(() => msg.remove(), 300);
        }, 4000 + (idx * 500));
    });
});
