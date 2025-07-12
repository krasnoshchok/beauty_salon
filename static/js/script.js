// Enhanced Beauty Salon JavaScript with improved functionality

// Utility functions
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

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

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Notification system
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-message">${message}</span>
        <button class="notification-close" aria-label="Close notification">&times;</button>
    `;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        background: ${getNotificationColor(type)};
        z-index: 3000;
        animation: slideInRight 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 300px;
        max-width: 500px;
    `;

    document.body.appendChild(notification);

    // Close button handler
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.style.cssText = `
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    `;

    const removeNotification = () => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    };

    closeBtn.addEventListener('click', removeNotification);

    if (duration > 0) {
        setTimeout(removeNotification, duration);
    }
}

function getNotificationColor(type) {
    const colors = {
        success: '#4CAF50',
        error: '#f44336',
        warning: '#ff9800',
        info: '#2196F3'
    };
    return colors[type] || colors.info;
}

// Smooth scrolling initialization
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    if (navLinks.length > 0) {
        navLinks.forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const target = document.querySelector(targetId);

                if (target) {
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
}

// Language selector initialization
function initLanguageSelector() {
    const languageSelector = document.querySelector('.language-selector');
    const currentLang = document.querySelector('.current-lang');

    if (languageSelector && currentLang) {
        // Handle click on language selector
        currentLang.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            languageSelector.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!languageSelector.contains(e.target)) {
                languageSelector.classList.remove('active');
            }
        });

        // Prevent dropdown from closing when clicking on language options
        const languageLinks = document.querySelectorAll('.language-dropdown a');
        languageLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.stopPropagation();
                // Add loading state
                this.style.opacity = '0.7';
                showNotification('Changing language...', 'info', 2000);
            });
        });

        // Keyboard navigation for language selector
        currentLang.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                languageSelector.classList.toggle('active');
            } else if (e.key === 'Escape') {
                languageSelector.classList.remove('active');
            }
        });
    }
}

// Mobile menu initialization
function initMobileMenu() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');

            // Update aria-expanded for accessibility
            const isExpanded = navMenu.classList.contains('active');
            this.setAttribute('aria-expanded', isExpanded);
        });

        // Close mobile menu when clicking on a nav link
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
            });
        });
    }
}

// Enhanced navbar scroll effects
function initNavbarScrollEffects() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    const handleScroll = throttle(function() {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 30px rgba(0, 0, 0, 0.15)';
            navbar.classList.add('scrolled');
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
            navbar.classList.remove('scrolled');
        }
    }, 16); // ~60fps

    window.addEventListener('scroll', handleScroll);
}

// Enhanced scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.classList.add('animated');
            }
        });
    }, observerOptions);

    // Observe elements with staggered animation
    const elements = document.querySelectorAll('.service-card, .contact-item, .gallery-item, .review-card, .info-item');
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = `all 0.6s ease ${index * 0.1}s`;
        observer.observe(el);
    });
}

// Enhanced gallery with keyboard navigation and accessibility
function initGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    if (galleryItems.length === 0) return;

    galleryItems.forEach((item, index) => {
        // Make gallery items focusable
        item.setAttribute('tabindex', '0');
        item.setAttribute('role', 'button');
        item.setAttribute('aria-label', `Open gallery image ${index + 1}`);

        const clickHandler = () => openLightbox(item, index);
        const keyHandler = (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openLightbox(item, index);
            }
        };

        item.addEventListener('click', clickHandler);
        item.addEventListener('keydown', keyHandler);
    });
}

function openLightbox(item, currentIndex) {
    const img = item.querySelector('img');
    if (!img) return;

    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = createLightboxElement(img.src, img.alt, currentIndex, galleryItems.length);

    document.body.appendChild(lightbox);
    document.body.style.overflow = 'hidden';

    // Focus management
    const closeBtn = lightbox.querySelector('.lightbox-close');
    closeBtn.focus();

    setupLightboxNavigation(lightbox, galleryItems, currentIndex);
}

function createLightboxElement(src, alt, currentIndex, totalImages) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-label', 'Image gallery viewer');
    lightbox.setAttribute('aria-modal', 'true');

    lightbox.innerHTML = `
        <div class="lightbox-content">
            <div class="lightbox-header">
                <span class="lightbox-counter">${currentIndex + 1} / ${totalImages}</span>
                <button class="lightbox-close" aria-label="Close gallery" title="Close (Esc)">&times;</button>
            </div>
            <div class="lightbox-body">
                ${currentIndex > 0 ? '<button class="lightbox-nav lightbox-prev" aria-label="Previous image" title="Previous (←)">&#8249;</button>' : ''}
                <img src="${src}" alt="${alt}" class="lightbox-image">
                ${currentIndex < totalImages - 1 ? '<button class="lightbox-nav lightbox-next" aria-label="Next image" title="Next (→)">&#8250;</button>' : ''}
            </div>
        </div>
    `;

    // Apply styles
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.95);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
        animation: fadeIn 0.3s ease;
    `;

    return lightbox;
}

function setupLightboxNavigation(lightbox, galleryItems, currentIndex) {
    const closeLightbox = () => {
        lightbox.style.animation = 'fadeOut 0.3s ease';
        document.body.style.overflow = '';
        setTimeout(() => {
            if (lightbox.parentNode) {
                lightbox.remove();
            }
        }, 300);
    };

    const navigateGallery = (direction) => {
        const newIndex = currentIndex + direction;
        if (newIndex >= 0 && newIndex < galleryItems.length) {
            closeLightbox();
            setTimeout(() => openLightbox(galleryItems[newIndex], newIndex), 100);
        }
    };

    // Event listeners
    const closeBtn = lightbox.querySelector('.lightbox-close');
    const prevBtn = lightbox.querySelector('.lightbox-prev');
    const nextBtn = lightbox.querySelector('.lightbox-next');

    closeBtn?.addEventListener('click', closeLightbox);
    prevBtn?.addEventListener('click', () => navigateGallery(-1));
    nextBtn?.addEventListener('click', () => navigateGallery(1));

    // Background click to close
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });

    // Keyboard navigation
    const handleKeydown = (e) => {
        switch (e.key) {
            case 'Escape':
                closeLightbox();
                break;
            case 'ArrowLeft':
                if (currentIndex > 0) navigateGallery(-1);
                break;
            case 'ArrowRight':
                if (currentIndex < galleryItems.length - 1) navigateGallery(1);
                break;
            case 'Tab':
                // Trap focus within lightbox
                const focusableElements = lightbox.querySelectorAll('button');
                const firstFocusable = focusableElements[0];
                const lastFocusable = focusableElements[focusableElements.length - 1];

                if (e.shiftKey && e.target === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                } else if (!e.shiftKey && e.target === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
                break;
        }
    };

    document.addEventListener('keydown', handleKeydown);

    // Store reference to remove listener when lightbox closes
    lightbox.keydownHandler = handleKeydown;

    // Remove event listener when lightbox is removed
    const originalRemove = lightbox.remove;
    lightbox.remove = function() {
        document.removeEventListener('keydown', this.keydownHandler);
        originalRemove.call(this);
    };
}

// Contact form initialization
function initContactForm() {
    const contactForm = document.querySelector('#contact-form');
    if (!contactForm) return;

    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(this);
        const data = Object.fromEntries(formData);

        // Clear previous error states
        clearFormErrors(this);

        // Validate form
        const errors = validateContactForm(data);

        if (errors.length > 0) {
            displayFormErrors(this, errors);
            showNotification('Please correct the errors in the form', 'error');
            return;
        }

        // Simulate form submission
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        // Simulate API call
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
            showNotification('Thank you for your message! We\'ll get back to you soon.', 'success');
            this.reset();
        }, 2000);
    });
}

function validateContactForm(data) {
    const errors = [];

    if (!data.name || data.name.trim().length < 2) {
        errors.push({ field: 'name', message: 'Name must be at least 2 characters long' });
    }

    if (!data.email || !isValidEmail(data.email)) {
        errors.push({ field: 'email', message: 'Please enter a valid email address' });
    }

    if (!data.message || data.message.trim().length < 10) {
        errors.push({ field: 'message', message: 'Message must be at least 10 characters long' });
    }

    return errors;
}

function clearFormErrors(form) {
    const errorElements = form.querySelectorAll('.field-error');
    errorElements.forEach(el => el.remove());

    const invalidFields = form.querySelectorAll('.invalid');
    invalidFields.forEach(field => field.classList.remove('invalid'));
}

function displayFormErrors(form, errors) {
    errors.forEach(error => {
        const field = form.querySelector(`[name="${error.field}"]`);
        if (field) {
            field.classList.add('invalid');

            const errorElement = document.createElement('div');
            errorElement.className = 'field-error';
            errorElement.textContent = error.message;
            errorElement.style.cssText = 'color: #f44336; font-size: 12px; margin-top: 4px;';

            field.parentNode.appendChild(errorElement);
        }
    });
}

// Add required CSS animations
function addRequiredStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        
        @keyframes slideInRight {
            from { 
                transform: translateX(100%); 
                opacity: 0; 
            }
            to { 
                transform: translateX(0); 
                opacity: 1; 
            }
        }
        
        @keyframes slideOutRight {
            from { 
                transform: translateX(0); 
                opacity: 1; 
            }
            to { 
                transform: translateX(100%); 
                opacity: 0; 
            }
        }
        
        .lightbox-content {
            position: relative;
            max-width: 90vw;
            max-height: 90vh;
            animation: zoomIn 0.3s ease;
        }
        
        .lightbox-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
        }
        
        .lightbox-close, .lightbox-nav {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 10px;
            border-radius: 50%;
            transition: background 0.3s ease;
        }
        
        .lightbox-close:hover, .lightbox-nav:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .lightbox-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            font-size: 36px;
            z-index: 10;
        }
        
        .lightbox-prev {
            left: 20px;
        }
        
        .lightbox-next {
            right: 20px;
        }
        
        .lightbox-image {
            max-width: 100%;
            max-height: 80vh;
            object-fit: contain;
            display: block;
        }
        
        @keyframes zoomIn {
            from { 
                transform: scale(0.8); 
                opacity: 0; 
            }
            to { 
                transform: scale(1); 
                opacity: 1; 
            }
        }
        
        .gallery-item:focus {
            outline: 2px solid #007bff;
            outline-offset: 2px;
        }
        
        .invalid {
            border-color: #f44336 !important;
            box-shadow: 0 0 0 2px rgba(244, 67, 54, 0.2) !important;
        }
        
        .notification {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .notification-close:hover {
            opacity: 0.8;
        }
    `;
    document.head.appendChild(style);
}

// Performance monitoring
function initPerformanceMonitoring() {
    // Monitor scroll performance
    let scrolling = false;
    window.addEventListener('scroll', () => {
        if (!scrolling) {
            requestAnimationFrame(() => {
                scrolling = false;
            });
            scrolling = true;
        }
    });

    // Monitor page load performance
    window.addEventListener('load', () => {
        if ('performance' in window) {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log(`Page loaded in ${loadTime}ms`);

            if (loadTime > 3000) {
                console.warn('Page load time is slow. Consider optimizing images and resources.');
            }
        }
    });
}

// Main initialization function
function initializeApp() {
    try {
        addRequiredStyles();
        initSmoothScrolling();
        initLanguageSelector();
        initMobileMenu();
        initNavbarScrollEffects();
        initScrollAnimations();
        initGallery();
        initContactForm();
        initPerformanceMonitoring();

        console.log('Beauty Salon app initialized successfully');
    } catch (error) {
        console.error('Error initializing app:', error);
        showNotification('An error occurred while loading the page. Please refresh.', 'error');
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}