document.addEventListener('DOMContentLoaded', () => {

    // 1. Page load fade staggered via IntersectionObserver
    const observer = new IntersectionObserver((entries) => {
        let delayCount = 0;
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('is-visible');
                }, delayCount * 60);
                delayCount++;
                observer.unobserve(entry.target);
            }
        });
    }, { rootMargin: '0px 0px -20px 0px', threshold: 0.1 });

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

    // 2. Button loading state
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('loading')) {
                submitBtn.classList.add('loading');
                submitBtn.style.width = submitBtn.offsetWidth + 'px'; // maintain size
                submitBtn.style.pointerEvents = 'none';
                
                // Inject SVG inline
                const spinner = `<svg style="width:14px; height:14px; margin-right:8px; animation:rotate 1.5s linear infinite;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="45 100" stroke-linecap="round"></circle></svg>`;
                submitBtn.innerHTML = spinner + "Loading...";
            }
        });
    });

    if (!document.getElementById('spinner-keyframes')) {
        const style = document.createElement('style');
        style.id = 'spinner-keyframes';
        style.innerHTML = `@keyframes rotate { 100% { transform: rotate(360deg); } }`;
        document.head.appendChild(style);
    }

    // 3. Active nav highlight auto-detect
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-link, .nav-links a').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });

    // 4. Smooth anchor scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if(target) target.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // 5. Flash message dismissal
    document.querySelectorAll('.flash-msg').forEach((msg, idx) => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-5px)';
            msg.style.transition = 'all 0.3s ease';
            setTimeout(() => msg.remove(), 300);
        }, 4000 + (idx * 500));
    });

    // 6. Notification bell polling (every 15 seconds)
    function pollNotifications() {
        fetch('/api/notifications')
            .then(r => r.json())
            .then(data => {
                const badge        = document.getElementById('notif-badge');
                const sidebarBadge = document.getElementById('sidebar-notif-badge');
                if (!badge) return;
                if (data.count > 0) {
                    badge.textContent  = data.count;
                    badge.style.display = 'flex';
                    if (sidebarBadge) {
                        sidebarBadge.textContent  = data.count;
                        sidebarBadge.style.display = 'inline';
                    }
                } else {
                    badge.style.display = 'none';
                    if (sidebarBadge) sidebarBadge.style.display = 'none';
                }
            })
            .catch(() => {});  // silently fail if not logged in
    }

    // Run immediately + every 15s
    if (document.getElementById('notif-badge')) {
        pollNotifications();
        setInterval(pollNotifications, 15000);
    }

});
