/**
 * Main JavaScript file for UniVerse application
 * Handles common functionality across all pages
 */

(function() {
    'use strict';

    /**
     * Initialize the application when DOM is ready
     */
    function initializeApplication() {
        console.log('UniVerse application initialized');
        updateCopyrightYear();
        enableProfessorAvailabilitySearchAutoSubmit();
    }

    /**
     * Update the copyright year in the footer
     */
    function updateCopyrightYear() {
        const yearElement = document.getElementById('year');
        if (yearElement) {
            yearElement.textContent = new Date().getFullYear();
        }
    }

    function enableProfessorAvailabilitySearchAutoSubmit() {
        const form = document.querySelector('form[action*="timetable"]');
        if (!form) return;
        const searchInput = form.querySelector('input[name="search"]');
        if (!searchInput) return;
        let timer;
        searchInput.addEventListener('input', function() {
            clearTimeout(timer);
            timer = setTimeout(() => {
                form.submit();
            }, 350);
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeApplication);
    } else {
        initializeApplication();
    }
})();
