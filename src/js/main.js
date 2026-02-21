/**
 * JOKESSHOTS — Portfolio Interactions
 * Mobile nav, category filter, scroll reveal, lightbox, parallax, accordions
 */

(function () {
    'use strict';

    // === MOBILE NAV ===
    const navToggle = document.getElementById('navToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileLinks = document.querySelectorAll('.mobile-menu-link');

    if (navToggle && mobileMenu) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        });

        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // === CATEGORY FILTER ===
    function initFilter() {
        const filterBtns = document.querySelectorAll('.filter-btn');
        const galleryItems = document.querySelectorAll('.gallery-item');

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.dataset.filter;

                // Update active button
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Filter items
                galleryItems.forEach(item => {
                    if (filter === 'all' || item.dataset.category === filter) {
                        item.classList.remove('hidden');
                    } else {
                        item.classList.add('hidden');
                    }
                });
            });
        });
    }

    // === SCROLL REVEAL ===
    function initScrollReveal() {
        const revealSelectors = [
            '.gallery-item',
            '.section-header',
            '.about-image',
            '.about-content',
            '.contact-box',
            '.why-text',
            '.faq-header',
            '.accordion-list',
            '.footer-top'
        ];

        revealSelectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(el => {
                el.classList.add('reveal');
            });
        });

        const revealElements = document.querySelectorAll('.reveal');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.08,
            rootMargin: '0px 0px -30px 0px'
        });

        revealElements.forEach(el => observer.observe(el));
    }

    // === ACCORDION (Services & FAQ) ===
    function initAccordions() {
        const accordionHeaders = document.querySelectorAll('.accordion-header');

        accordionHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const item = header.parentElement;
                const body = item.querySelector('.accordion-body');
                const content = item.querySelector('.accordion-content');
                const isActive = item.classList.contains('active');

                // Close all items in the same accordion list
                const list = item.closest('.accordion-list');
                if (list) {
                    list.querySelectorAll('.accordion-item.active').forEach(activeItem => {
                        if (activeItem !== item) {
                            activeItem.classList.remove('active');
                            const activeBody = activeItem.querySelector('.accordion-body');
                            activeBody.style.maxHeight = '0';
                            activeItem.querySelector('.accordion-header').setAttribute('aria-expanded', 'false');
                        }
                    });
                }

                // Toggle current item
                if (isActive) {
                    item.classList.remove('active');
                    body.style.maxHeight = '0';
                    header.setAttribute('aria-expanded', 'false');
                } else {
                    item.classList.add('active');
                    body.style.maxHeight = content.scrollHeight + 'px';
                    header.setAttribute('aria-expanded', 'true');
                }
            });
        });
    }

    // === LIGHTBOX ===
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxClose = document.getElementById('lightboxClose');
    const lightboxPrev = document.getElementById('lightboxPrev');
    const lightboxNext = document.getElementById('lightboxNext');
    const lightboxCounter = document.getElementById('lightboxCounter');
    let currentIndex = 0;
    let images = [];
    let imageElements = [];

    function initLightbox() {
        const galleryItems = document.querySelectorAll('.gallery-item');
        galleryItems.forEach((item, i) => {
            const img = item.querySelector('img');
            // Skip items that link to sub-pages (have real href, not "#")
            const href = item.getAttribute('href');
            if (href && href !== '#' && !href.startsWith('#')) return;
            if (img) {
                images.push(img.src);
                imageElements.push(item);
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    openLightbox(i);
                });
            }
        });
    }

    function updateCounter() {
        if (lightboxCounter) {
            lightboxCounter.textContent = `${currentIndex + 1} / ${images.length}`;
        }
    }

    function openLightbox(index) {
        currentIndex = index;
        lightboxImg.src = images[currentIndex];
        updateCounter();
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        lightboxImg.src = images[currentIndex];
        updateCounter();
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        lightboxImg.src = images[currentIndex];
        updateCounter();
    }

    if (lightbox) {
        lightboxClose.addEventListener('click', closeLightbox);
        lightboxNext.addEventListener('click', nextImage);
        lightboxPrev.addEventListener('click', prevImage);

        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) closeLightbox();
        });

        // Keyboard nav
        document.addEventListener('keydown', (e) => {
            if (!lightbox.classList.contains('active')) return;
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowRight') nextImage();
            if (e.key === 'ArrowLeft') prevImage();
        });

        // Touch swipe support
        let touchStartX = 0;
        lightbox.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        lightbox.addEventListener('touchend', (e) => {
            const diff = touchStartX - e.changedTouches[0].screenX;
            if (Math.abs(diff) > 50) {
                diff > 0 ? nextImage() : prevImage();
            }
        }, { passive: true });
    }

    // === HERO PARALLAX ===
    const hero = document.getElementById('hero');
    const heroContent = hero ? hero.querySelector('.hero-content') : null;
    const heroScroll = hero ? hero.querySelector('.hero-scroll') : null;

    function initParallax() {
        if (!hero || !heroContent) return;

        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            const heroHeight = hero.offsetHeight;

            if (scrollY < heroHeight) {
                const progress = scrollY / heroHeight;
                heroContent.style.transform = `translateY(${scrollY * 0.3}px)`;
                heroContent.style.opacity = 1 - progress * 1.8;
                if (heroScroll) {
                    heroScroll.style.opacity = Math.max(0, 0.5 - progress * 2);
                }
            }
        }, { passive: true });
    }

    // === SMOOTH SCROLL ===
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href === '#') return;
            const target = document.getElementById(href.substring(1));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // === EMAIL OBFUSCATION (anti-harvesting) ===
    function getEmail() {
        var u = 'hello'; var d = 'jokesshots.com';
        return u + '@' + d;
    }

    function initEmailLinks() {
        // Render obfuscated email into footer links
        document.querySelectorAll('.js-email-link').forEach(function(el) {
            var addr = getEmail();
            el.href = 'mailto:' + addr;
            el.textContent = addr;
        });
    }

    // === CONTACT FORM & TEMPLATE CHIPS ===
    function initContactForm() {
        const chips = document.querySelectorAll('.template-chip');
        const textarea = document.querySelector('.contact-textarea');
        const form = document.getElementById('contactForm');

        if (chips.length && textarea) {
            chips.forEach(chip => {
                chip.addEventListener('click', () => {
                    const template = chip.dataset.template;
                    const wasActive = chip.classList.contains('active');
                    chips.forEach(c => c.classList.remove('active'));

                    if (wasActive) {
                        textarea.value = '';
                    } else {
                        chip.classList.add('active');
                        textarea.value = template;
                        textarea.focus();
                        textarea.setSelectionRange(template.length, template.length);
                    }
                });
            });

            textarea.addEventListener('input', () => {
                const activeChip = document.querySelector('.template-chip.active');
                if (activeChip && textarea.value !== activeChip.dataset.template) {
                    activeChip.classList.remove('active');
                }
            });
        }

        // Form submission via mailto (constructed at runtime to avoid scraping)
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                var name = form.querySelector('[name="name"]').value.trim();
                var email = form.querySelector('[name="email"]').value.trim();
                var message = form.querySelector('[name="message"]').value.trim();
                if (!name || !email || !message) return;
                var subject = encodeURIComponent('Inquiry from ' + name);
                var body = encodeURIComponent('Name: ' + name + '\nEmail: ' + email + '\n\n' + message);
                window.location.href = 'mailto:' + getEmail() + '?subject=' + subject + '&body=' + body;
            });
        }
    }

    // === RESPONSIVE VIDEO SOURCE ===
    function initResponsiveVideo() {
        const video = document.querySelector('.hero-video');
        if (!video) return;
        const isMobile = window.innerWidth < 768;
        const src = isMobile ? video.dataset.srcMobile : video.dataset.srcDesktop;
        if (src) {
            video.src = src;
            video.load();
        }
    }

    // === INIT ===
    document.addEventListener('DOMContentLoaded', () => {
        initResponsiveVideo();
        initFilter();
        initScrollReveal();
        initLightbox();
        initParallax();
        initAccordions();
        initEmailLinks();
        initContactForm();
    });

})();
