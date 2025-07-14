            // Script for the loader to load on every new page for at least 0.4s
            document.addEventListener("DOMContentLoaded", () => {
                const loader = document.querySelector('.loader-container');

                function showLoader() {
                    loader.classList.remove('hidden');
                }

                function hideLoader() {
                    setTimeout(() => {
                        loader.classList.add('hidden');
                    }, 400); // Minimum delay to show the loader
                }

                document.querySelectorAll('a').forEach(link => {
                    link.addEventListener('click', (e) => {
                        const url = link.getAttribute('href');

                        // Skip lightbox links
                        if (link.classList.contains('lightbox')) {
                            return; // Ignore loader for lightbox
                        }

                        // Check if the link is internal (same origin or relative URL)
                        const isInternal = url && (url.startsWith('/') || url.startsWith(window.location.origin));

                        if (isInternal) {
                            showLoader();
                        } else {
                            e.preventDefault(); // Optional: prevent external links from triggering loader
                            window.location.href = url; // Redirect to external site without showing the loader
                        }
                    });
                });

                // Hide the loader after the page fully loads
                window.addEventListener('load', hideLoader);

                // Reset the loader when navigating back
                window.addEventListener('pageshow', (event) => {
                    if (event.persisted) {
                        loader.classList.add('hidden');
                    }
                });
            });
