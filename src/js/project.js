/**
 * JOKESSHOTS — Project Page Interactions
 * Lightbox, scroll reveal, mobile nav
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

    // === LIGHTBOX ===
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxClose = document.getElementById('lightboxClose');
    const lightboxPrev = document.getElementById('lightboxPrev');
    const lightboxNext = document.getElementById('lightboxNext');
    const lightboxCounter = document.getElementById('lightboxCounter');
    let currentIndex = 0;
    let fullImages = [];

    function initProjectLightbox() {
        const photos = document.querySelectorAll('.project-photo');
        photos.forEach((photo, i) => {
            const fullSrc = photo.dataset.full;
            if (fullSrc) {
                fullImages.push(fullSrc);
                photo.addEventListener('click', () => openLightbox(i));
            }
        });
    }

    function updateCounter() {
        if (lightboxCounter) {
            lightboxCounter.textContent = `${currentIndex + 1} / ${fullImages.length}`;
        }
    }

    function openLightbox(index) {
        currentIndex = index;
        lightboxImg.src = fullImages[currentIndex];
        updateCounter();
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % fullImages.length;
        lightboxImg.src = fullImages[currentIndex];
        updateCounter();
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + fullImages.length) % fullImages.length;
        lightboxImg.src = fullImages[currentIndex];
        updateCounter();
    }

    if (lightbox) {
        lightboxClose.addEventListener('click', closeLightbox);
        lightboxNext.addEventListener('click', nextImage);
        lightboxPrev.addEventListener('click', prevImage);

        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) closeLightbox();
        });

        document.addEventListener('keydown', (e) => {
            if (!lightbox.classList.contains('active')) return;
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowRight') nextImage();
            if (e.key === 'ArrowLeft') prevImage();
        });

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

    // === SCROLL REVEAL ===
    function initScrollReveal() {
        const elements = document.querySelectorAll('.project-photo, .project-bio');
        elements.forEach(el => el.classList.add('reveal'));

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
    }

    // === EMAIL OBFUSCATION ===
    function initEmailLinks() {
        var u = 'hello'; var d = 'jokesshots.com';
        var addr = u + '@' + d;
        document.querySelectorAll('.js-email-link').forEach(function(el) {
            el.href = 'mailto:' + addr;
            el.textContent = addr;
        });
    }

    // === INIT ===
    document.addEventListener('DOMContentLoaded', () => {
        initProjectLightbox();
        initScrollReveal();
        initEmailLinks();
    });

})();
