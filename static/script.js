document.addEventListener("DOMContentLoaded", () => {
  // 1. IntersectionObserver for scroll animations
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };
  
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        // Add fade-in class and stagger via inline style delay
        entry.target.classList.add('fade-in');
        entry.target.style.animationDelay = `${index * 0.1}s`;
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  // Select elements to animate in
  const animateElements = document.querySelectorAll('.stat-card, .skill-card, .card');
  animateElements.forEach(el => {
    el.style.opacity = '0'; // Hide initially
    observer.observe(el);
  });

  // 2. Ripple effect on buttons
  const buttons = document.querySelectorAll('.btn-primary, .nav-cta');
  
  buttons.forEach(button => {
    button.addEventListener('mousedown', function (e) {
      const x = e.clientX - e.target.getBoundingClientRect().left;
      const y = e.clientY - e.target.getBoundingClientRect().top;
      
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      
      this.appendChild(ripple);
      
      setTimeout(() => {
        ripple.remove();
      }, 500);
    });
  });

  // Invalid shake demo function (can be called by forms)
  window.triggerInvalidShake = function(elementId) {
    const el = document.getElementById(elementId);
    if(el) {
      el.classList.remove('shake');
      void el.offsetWidth; // trigger reflow
      el.classList.add('shake');
    }
  };
});
