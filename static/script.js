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

  // ----- NOTIFICATION SYSTEM -----
  const bellIcon = document.getElementById('bellIcon');
  const notifDropdown = document.getElementById('notifDropdown');
  const notifContainer = document.getElementById('notifContainer');
  const notifList = document.getElementById('notifList');
  const notifBadge = document.getElementById('notifBadge');
  const clearNotifs = document.getElementById('clearNotifs');
  
  // Optional: Sound for new messages
  // const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  function playNotificationSound() {
    // Only works after user interaction due to browser policies, so disabled by default 
    // or triggered intelligently.
    // const oscillator = audioCtx.createOscillator();
    // const gainNode = audioCtx.createGain();
    // oscillator.type = 'sine';
    // oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
    // oscillator.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
    // gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
    // gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
    // oscillator.connect(gainNode);
    // gainNode.connect(audioCtx.destination);
    // oscillator.start();
    // oscillator.stop(audioCtx.currentTime + 0.5);
  }

  let totalUnread = 0;
  let notificationsData = [];

  function formatTimeAgo(dateString) {
    const date = new Date(dateString);
    const seconds = Math.floor((new Date() - date) / 1000);
    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + " yrs ago";
    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + " mos ago";
    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + " days ago";
    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + " hrs ago";
    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + " mins ago";
    return "Just now";
  }

  function renderNotifications() {
    if(!notifList) return;
    notifList.innerHTML = '';
    
    if(notificationsData.length === 0) {
      notifList.innerHTML = '<div class="notif-empty">No notifications</div>';
      notifBadge.style.display = 'none';
      return;
    }

    let unreadCount = 0;
    notificationsData.forEach(notif => {
      if(!notif.read_status) unreadCount++;
      
      const el = document.createElement('div');
      el.className = `notif-item ${!notif.read_status ? 'unread' : ''}`;
      
      // Determine icon based on type
      let svg = '<svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>';
      if (notif.type === 'session') {
        svg = '<svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>';
      } else if (notif.type === 'feedback') {
        svg = '<svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path></svg>';
      }

      el.innerHTML = `
        <div class="notif-icon">${svg}</div>
        <div class="notif-content">
          <div class="notif-message">${notif.message}</div>
          <div class="notif-time">${formatTimeAgo(notif.timestamp)}</div>
        </div>
      `;
      
      el.addEventListener('click', () => {
        if(!notif.read_status) {
          fetch(`/api/notifications/${notif._id}/read`, { method: 'POST' })
            .then(() => fetchNotifications());
        }
      });
      
      notifList.appendChild(el);
    });

    if(unreadCount > totalUnread) {
      // New notification arrived!
      playNotificationSound();
    }
    
    totalUnread = unreadCount;
    notifBadge.style.display = unreadCount > 0 ? 'block' : 'none';
  }

  function fetchNotifications() {
    fetch('/api/notifications')
      .then(r => r.json())
      .then(data => {
        if(data.notifications) {
          if (notifContainer) notifContainer.style.display = 'block'; // Show if returned
          notificationsData = data.notifications;
          renderNotifications();
        }
      }).catch(err => console.log('Err fetching notifs', err));
  }

  if (bellIcon) {
    bellIcon.addEventListener('click', (e) => {
      e.stopPropagation();
      notifDropdown.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
      if(!notifContainer.contains(e.target)) {
        notifDropdown.classList.remove('show');
      }
    });

    clearNotifs.addEventListener('click', () => {
      fetch('/api/notifications/clear', { method: 'POST' })
        .then(() => {
          notificationsData = [];
          renderNotifications();
        });
    });

    // Start polling immediately, then every 10 seconds
    fetchNotifications();
    setInterval(fetchNotifications, 10000);
  }

});
