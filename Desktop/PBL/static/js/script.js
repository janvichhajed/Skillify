document.addEventListener('DOMContentLoaded', () => {
    // Page Fade-in Effect
    document.body.classList.add('fade-in');

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
            
            // Subtle button loading state
            const btn = form.querySelector('button[type="submit"]');
            if (btn && form.checkValidity()) {
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                btn.style.opacity = '0.8';
            }
        }, false);
    });

    // Button Click Feedback (Scale Effect)
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mousedown', () => btn.style.transform = 'scale(0.95)');
        btn.addEventListener('mouseup', () => btn.style.transform = '');
        btn.addEventListener('mouseleave', () => btn.style.transform = '');
    });
});

