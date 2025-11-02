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

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeApplication);
    } else {
        initializeApplication();
    }
})();
