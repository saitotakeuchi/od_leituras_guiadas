/**
 * Leitura Guiada - Script de sincronização de áudio e texto
 * Objeto Educacional - Positivo
 */

(function() {
    'use strict';

    // DOM Elements
    const audio = document.getElementById('audio');
    const playBtn = document.getElementById('play-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const progressBar = document.getElementById('progress-bar');
    const textoCompletoBtn = document.getElementById('texto-completo-btn');
    const modalOverlay = document.getElementById('modal-overlay');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const voltarBtn = document.getElementById('voltar-btn');
    const zoomBtn = document.getElementById('zoom-btn');
    const modalImage = document.getElementById('modal-image');
    const zoomOverlay = document.getElementById('zoom-overlay');
    const closeZoomBtn = document.getElementById('close-zoom-btn');
    const lyricsContainer = document.getElementById('lyrics');
    const container = document.getElementById('main-view');
    const readingContent = document.querySelector('.reading-content');

    // Get all text spans with timing data (word-by-word) - including title and text
    const textSpans = readingContent.querySelectorAll('span[data-start]');

    // Calculate the effective duration based on the last word's end time
    const lastSpan = textSpans[textSpans.length - 1];
    const effectiveDuration = lastSpan ? parseFloat(lastSpan.dataset.end) : 0;

    // State
    let isPlaying = false;

    // Initialize
    function init() {
        setupAudioEvents();
        setupControlEvents();
        setupModalEvents();
        setupKeyboardNavigation();
    }

    // Audio Events
    function setupAudioEvents() {
        // Use 100 as max for simplicity - we'll map times to percentage
        progressBar.max = 100;

        audio.addEventListener('timeupdate', function() {
            updateProgressBar();
            updateTextHighlight();
        });

        audio.addEventListener('ended', function() {
            isPlaying = false;
            updatePlayPauseState();
            resetTextHighlight();
            // Ensure progress bar is at 100% when audio ends
            progressBar.value = 100;
        });

        audio.addEventListener('play', function() {
            isPlaying = true;
            updatePlayPauseState();
        });

        audio.addEventListener('pause', function() {
            isPlaying = false;
            updatePlayPauseState();
        });
    }

    // Control Events
    function setupControlEvents() {
        playBtn.addEventListener('click', function() {
            audio.play();
        });

        pauseBtn.addEventListener('click', function() {
            audio.pause();
        });

        progressBar.addEventListener('input', function() {
            // Map percentage back to time
            audio.currentTime = (progressBar.value / 100) * effectiveDuration;
            updateTextHighlight();
        });

        progressBar.addEventListener('change', function() {
            audio.currentTime = (progressBar.value / 100) * effectiveDuration;
        });
    }

    // Modal Events
    function setupModalEvents() {
        textoCompletoBtn.addEventListener('click', openModal);
        closeModalBtn.addEventListener('click', closeModal);
        voltarBtn.addEventListener('click', closeModal);
        zoomBtn.addEventListener('click', openZoom);
        closeZoomBtn.addEventListener('click', closeZoom);

        // Close modal/zoom with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                if (zoomOverlay.classList.contains('active')) {
                    closeZoom();
                } else if (!modalOverlay.hidden) {
                    closeModal();
                }
            }
        });
    }

    // Keyboard Navigation
    function setupKeyboardNavigation() {
        document.addEventListener('keydown', function(e) {
            // Space bar to play/pause (when not in modal)
            if (e.key === ' ' && modalOverlay.hidden && e.target.tagName !== 'BUTTON') {
                e.preventDefault();
                if (isPlaying) {
                    audio.pause();
                } else {
                    audio.play();
                }
            }

            // Arrow keys for seeking (5 seconds)
            if (e.key === 'ArrowLeft' && modalOverlay.hidden) {
                audio.currentTime = Math.max(0, audio.currentTime - 5);
            }
            if (e.key === 'ArrowRight' && modalOverlay.hidden) {
                audio.currentTime = Math.min(audio.duration, audio.currentTime + 5);
            }
        });
    }

    // Update Progress Bar
    function updateProgressBar() {
        // Map current time to percentage (0-100), reaching 100% when reading ends
        const percentage = Math.min((audio.currentTime / effectiveDuration) * 100, 100);
        progressBar.value = percentage;
    }

    // Update Play/Pause Button State
    function updatePlayPauseState() {
        if (isPlaying) {
            playBtn.classList.remove('active');
            pauseBtn.classList.add('active');
            playBtn.setAttribute('aria-pressed', 'false');
            pauseBtn.setAttribute('aria-pressed', 'true');
        } else {
            playBtn.classList.add('active');
            pauseBtn.classList.remove('active');
            playBtn.setAttribute('aria-pressed', 'true');
            pauseBtn.setAttribute('aria-pressed', 'false');
        }
    }

    // Update Text Highlight (Karaoke Effect - Word by Word)
    function updateTextHighlight() {
        const currentTime = audio.currentTime;
        let activeSpan = null;

        // Update each word span based on current time
        textSpans.forEach(function(span) {
            const startTime = parseFloat(span.dataset.start);
            const endTime = parseFloat(span.dataset.end);

            span.classList.remove('active', 'past');

            if (currentTime >= startTime && currentTime < endTime) {
                // Currently being spoken
                span.classList.add('active');
                activeSpan = span;
            } else if (currentTime >= endTime) {
                // Already spoken
                span.classList.add('past');
            }
            // Future words have no class (default styling)
        });

        // Auto-scroll to keep active word visible
        if (activeSpan && isPlaying) {
            scrollToActiveWord(activeSpan);
        }
    }

    // Scroll to keep active word visible
    function scrollToActiveWord(activeSpan) {
        const containerRect = container.getBoundingClientRect();
        const spanRect = activeSpan.getBoundingClientRect();

        // Calculate the visible area (accounting for fixed player/footer on mobile)
        const visibleTop = containerRect.top;
        const visibleBottom = containerRect.height * 0.6; // Upper 60% of container

        // Check if the active word is outside the visible area
        if (spanRect.top < visibleTop || spanRect.bottom > visibleBottom) {
            activeSpan.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }
    }

    // Reset Text Highlight
    function resetTextHighlight() {
        textSpans.forEach(function(span) {
            span.classList.remove('active', 'past');
        });
    }

    // Modal Functions
    function openModal() {
        // Pause audio when opening modal
        if (isPlaying) {
            audio.pause();
        }

        modalOverlay.hidden = false;
        modalOverlay.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';

        // Focus on close button for accessibility
        closeModalBtn.focus();
    }

    function closeModal() {
        modalOverlay.hidden = true;
        modalOverlay.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';

        // Return focus to the button that opened the modal
        textoCompletoBtn.focus();
    }

    function openZoom() {
        zoomOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        closeZoomBtn.focus();
    }

    function closeZoom() {
        zoomOverlay.classList.remove('active');
        document.body.style.overflow = 'hidden'; // Keep hidden since modal is still open
        zoomBtn.focus();
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
