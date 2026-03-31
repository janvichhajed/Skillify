document.addEventListener('DOMContentLoaded', () => {
    // Form verification sweep
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
            
            const btn = form.querySelector('button[type="submit"]');
            if (btn && form.checkValidity()) {
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span><span style="opacity: 0.8">Processing...</span>';
                btn.style.pointerEvents = 'none'; // Prevent double clicking
                btn.style.transform = 'scale(0.98)';
                btn.classList.add('disabled');
            }
        }, false);
    });

    // Magnetic / Squeeze Button interactions
    document.querySelectorAll('.btn-ultra, .btn-accent-glow').forEach(btn => {
        btn.addEventListener('mousedown', () => btn.style.transform = 'scale(0.95)');
        btn.addEventListener('mouseup', () => {
            btn.style.transform = '';
            // Restores the transform lift from CSS on hover
            if(btn.matches(':hover') && !btn.classList.contains('disabled')) {
                btn.style.transform = 'translateY(-2px)';
            }
        });
        btn.addEventListener('mouseleave', () => btn.style.transform = '');
    });

    // Mobile Sidebar Toggle
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebarCloseBtn = document.getElementById('sidebarCloseBtn');
    const sidebar = document.querySelector('.sidebar');

    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', () => sidebar.classList.add('show'));
    }

    if (sidebarCloseBtn && sidebar) {
        sidebarCloseBtn.addEventListener('click', () => sidebar.classList.remove('show'));
    }

    // Advanced features: Reveal elements on scroll using Intersection Observer
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Determine stagger delay based on data attribute or index within parent
                const staggerIndex = entry.target.dataset.stagger || 1;
                entry.target.style.animationDelay = `${staggerIndex * 0.1}s`;
                entry.target.classList.add('slide-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Grab elements that should animate in when scrolled
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        // Init opacity and clear transform before observation kicks in via class
        el.style.opacity = '0'; 
        observer.observe(el);
    });
});
