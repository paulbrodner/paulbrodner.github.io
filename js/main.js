---
layout: null
sitemap:
  exclude: 'yes'
---

(function() {
  'use strict';

  // Wait for DOM to be ready
  document.addEventListener('DOMContentLoaded', function() {
    initializePanelCover();
    initializeMobileMenu();
    // initializeThemeToggle(); // Disabled for now
    improveAccessibility();
  });

  function initializePanelCover() {
    const panelCover = document.querySelector('.panel-cover');
    const contentWrapper = document.querySelector('.content-wrapper');
    const blogButtons = document.querySelectorAll('a.blog-button');

    // Handle blog button clicks
    blogButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        if (panelCover.classList.contains('panel-cover--collapsed')) return;
        
        const currentWidth = panelCover.offsetWidth;
        
        if (currentWidth < 960) {
          panelCover.classList.add('panel-cover--collapsed');
          contentWrapper.classList.add('animated', 'slideInRight');
        } else {
          panelCover.style.maxWidth = currentWidth + 'px';
          animatePanelWidth(panelCover, '330px', '40%');
        }
      });
    });

    // Check if we should collapse panel on load
    if (window.location.hash === '#blog') {
      panelCover.classList.add('panel-cover--collapsed');
    }

    if (window.location.pathname !== '{{ site.baseurl }}/' && 
        window.location.pathname !== '{{ site.baseurl }}/index.html') {
      panelCover.classList.add('panel-cover--collapsed');
    }
  }

  function animatePanelWidth(element, maxWidth, width) {
    element.style.transition = 'max-width 0.4s ease, width 0.4s ease';
    element.style.maxWidth = maxWidth;
    element.style.width = width;
  }

  function initializeMobileMenu() {
    const mobileMenuBtn = document.querySelector('.btn-mobile-menu');
    const navigationWrapper = document.querySelector('.navigation-wrapper');
    const mobileMenuIcon = document.querySelector('.btn-mobile-menu__icon');
    
    if (!mobileMenuBtn) return;

    mobileMenuBtn.addEventListener('click', function() {
      navigationWrapper.classList.toggle('visible');
      navigationWrapper.classList.toggle('animated');
      navigationWrapper.classList.toggle('bounceInDown');
      
      // Toggle icon classes
      if (mobileMenuIcon.classList.contains('icon-list')) {
        mobileMenuIcon.classList.remove('icon-list');
        mobileMenuIcon.classList.add('icon-x-circle', 'animated', 'fadeIn');
      } else {
        mobileMenuIcon.classList.remove('icon-x-circle');
        mobileMenuIcon.classList.add('icon-list');
      }
    });

    // Close mobile menu when clicking a link
    const navLinks = document.querySelectorAll('.navigation-wrapper .blog-button');
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        if (window.innerWidth < 960) {
          navigationWrapper.classList.remove('visible');
          mobileMenuIcon.classList.remove('icon-x-circle');
          mobileMenuIcon.classList.add('icon-list');
        }
      });
    });
  }

  function initializeThemeToggle() {
    // Check for saved theme preference or default to 'light'
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Create theme toggle button
    const themeToggle = document.createElement('button');
    themeToggle.className = 'theme-toggle';
    themeToggle.setAttribute('aria-label', 'Toggle dark mode');
    themeToggle.innerHTML = currentTheme === 'dark' ? '☀️' : '🌙';
    document.body.appendChild(themeToggle);

    themeToggle.addEventListener('click', function() {
      const theme = document.documentElement.getAttribute('data-theme');
      const newTheme = theme === 'dark' ? 'light' : 'dark';
      
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      themeToggle.innerHTML = newTheme === 'dark' ? '☀️' : '🌙';
      
      // Smooth transition
      document.documentElement.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    });
  }

  function improveAccessibility() {
    // Add skip to content link
    const skipLink = document.createElement('a');
    skipLink.href = '#blog';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Skip to main content';
    skipLink.style.cssText = `
      position: absolute;
      top: -40px;
      left: 0;
      background: var(--primary-color);
      color: white;
      padding: 8px;
      text-decoration: none;
      z-index: 100;
    `;
    
    skipLink.addEventListener('focus', () => {
      skipLink.style.top = '0';
    });
    
    skipLink.addEventListener('blur', () => {
      skipLink.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);

    // Improve image alt attributes
    const images = document.querySelectorAll('img:not([alt])');
    images.forEach(img => {
      img.setAttribute('alt', '');
    });

    // Add ARIA labels to icon-only buttons/links
    const iconLinks = document.querySelectorAll('.navigation--social a');
    iconLinks.forEach(link => {
      const label = link.querySelector('.label');
      if (label) {
        link.setAttribute('aria-label', label.textContent);
      }
    });
  }

  // Lazy loading for images
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
            observer.unobserve(img);
          }
        }
      });
    });

    // Observe all images with data-src
    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href !== '#blog') {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });

  // Add keyboard navigation improvements
  document.addEventListener('keydown', function(e) {
    // ESC key closes mobile menu
    if (e.key === 'Escape') {
      const navigationWrapper = document.querySelector('.navigation-wrapper');
      const mobileMenuIcon = document.querySelector('.btn-mobile-menu__icon');
      
      if (navigationWrapper && navigationWrapper.classList.contains('visible')) {
        navigationWrapper.classList.remove('visible');
        if (mobileMenuIcon) {
          mobileMenuIcon.classList.remove('icon-x-circle');
          mobileMenuIcon.classList.add('icon-list');
        }
      }
    }

    // '/' key focuses search
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
      const searchInput = document.querySelector('#search-container input');
      if (searchInput && document.activeElement !== searchInput) {
        e.preventDefault();
        searchInput.focus();
      }
    }
  });

  // Performance: Debounce function for scroll/resize events
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Handle window resize
  let resizeTimer;
  window.addEventListener('resize', function() {
    document.body.classList.add('resize-animation-stopper');
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      document.body.classList.remove('resize-animation-stopper');
    }, 400);
  });

})();