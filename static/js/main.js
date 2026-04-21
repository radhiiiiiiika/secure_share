/**
 * SecureShare AES — Main JS
 * Place this file at: static/js/main.js
 */

'use strict';

// ============================================================
// AUTO-DISMISS ALERTS
// ============================================================
(function initAlerts() {
  document.querySelectorAll('.alert').forEach(alert => {
    // Auto-dismiss success/info alerts after 5s
    if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
      setTimeout(() => {
        alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-6px)';
        setTimeout(() => alert.remove(), 500);
      }, 5000);
    }
  });
})();

// ============================================================
// ACTIVE NAV HIGHLIGHTING
// ============================================================
(function highlightActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a, .sidebar-item').forEach(link => {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });
})();

// ============================================================
// TABLE ROW HIGHLIGHT ON CLICK
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('tbody tr').forEach(row => {
    row.addEventListener('click', function () {
      document.querySelectorAll('tbody tr.selected').forEach(r => r.classList.remove('selected'));
      this.classList.toggle('selected');
    });
  });
});

// ============================================================
// COPY TO CLIPBOARD UTILITY
// ============================================================
function copyToClipboard(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const original = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-check"></i>';
    btn.style.color = 'var(--green)';
    setTimeout(() => {
      btn.innerHTML = original;
      btn.style.color = '';
    }, 1800);
  });
}

// ============================================================
// FORM SUBMIT LOADING STATE
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function (e) {
      const submitBtn = this.querySelector('[type="submit"]');
      if (!submitBtn || submitBtn.disabled) return;
      const originalHTML = submitBtn.innerHTML;
      submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing...';
      submitBtn.disabled = true;
      // Re-enable after 10s fallback (in case of validation error)
      setTimeout(() => {
        submitBtn.innerHTML = originalHTML;
        submitBtn.disabled = false;
      }, 10000);
    });
  });
});

// ============================================================
// TOOLTIP INITIALIZATION (data-tooltip elements)
// ============================================================
// Handled entirely via CSS — no JS needed.

// ============================================================
// MODAL ESCAPE KEY CLOSE
// ============================================================
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay:not(.hidden)').forEach(m => m.classList.add('hidden'));
  }
});

// ============================================================
// ANIMATED NUMBER COUNTER (stat cards)
// ============================================================
function animateCounter(el, target, duration = 600) {
  const start = parseInt(el.textContent) || 0;
  const range = target - start;
  const startTime = performance.now();
  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(start + range * eased);
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.stat-value').forEach(el => {
    const val = parseInt(el.textContent);
    if (!isNaN(val) && val > 0) {
      el.textContent = '0';
      // Trigger after a short delay for stagger effect
      setTimeout(() => animateCounter(el, val), 200);
    }
  });
});

// ============================================================
// DOWNLOAD PROGRESS SIMULATION (if progress bar present)
// ============================================================
function simulateDownloadProgress(barId, fillId, onComplete) {
  const bar = document.getElementById(barId);
  const fill = document.getElementById(fillId);
  if (!bar || !fill) return;
  bar.style.display = '';
  let w = 0;
  const iv = setInterval(() => {
    w = Math.min(w + Math.random() * 12, 95);
    fill.style.width = w + '%';
    if (w >= 95) {
      clearInterval(iv);
      setTimeout(() => {
        fill.style.width = '100%';
        setTimeout(() => {
          bar.style.display = 'none';
          if (onComplete) onComplete();
        }, 400);
      }, 300);
    }
  }, 150);
}

// ============================================================
// SIDEBAR ACTIVE STATE (based on current URL)
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  document.querySelectorAll('.sidebar-item').forEach(item => {
    const href = item.getAttribute('href');
    if (href && (href === path || (path.startsWith(href) && href !== '/'))) {
      item.classList.add('active');
    }
  });
});

// ============================================================
// FILE CARD HOVER EFFECT (tilt on mouse move)
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.file-card').forEach(card => {
    card.addEventListener('mousemove', function (e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      const rotX = ((y - cy) / cy) * 3;
      const rotY = ((x - cx) / cx) * -3;
      this.style.transform = `perspective(600px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-2px)`;
    });
    card.addEventListener('mouseleave', function () {
      this.style.transform = '';
    });
  });
});

// ============================================================
// TABLE SORT (click column header)
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('table th[data-sortable]').forEach(th => {
    th.style.cursor = 'pointer';
    th.addEventListener('click', function () {
      const table = this.closest('table');
      const tbody = table.querySelector('tbody');
      const colIdx = Array.from(this.parentElement.children).indexOf(this);
      const asc = this.dataset.sortDir !== 'asc';
      this.dataset.sortDir = asc ? 'asc' : 'desc';

      const rows = Array.from(tbody.querySelectorAll('tr'));
      rows.sort((a, b) => {
        const aVal = a.children[colIdx]?.textContent.trim() || '';
        const bVal = b.children[colIdx]?.textContent.trim() || '';
        return asc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
      });
      rows.forEach(r => tbody.appendChild(r));
    });
  });
});

// ============================================================
// GLOBAL: expose helpers
// ============================================================
window.SecureShare = {
  copyToClipboard,
  animateCounter,
  simulateDownloadProgress,
};