document.addEventListener('DOMContentLoaded', () => {
    // Basic Form validation before submit
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Animate alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            // Optional auto dismiss for flash messages
            // alert.style.opacity = '0';
            // setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});
