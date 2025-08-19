// Main JavaScript for Ceiling Solutions Website

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initNavbar();
    initAnimations();
    initSmoothScroll();
    initFormValidation();
    initProductGallery();
    initProductGallery();
    initProductGallery();
    
    // Navbar scroll effect
    function initNavbar() {
        const navbar = document.querySelector('.navbar');
        
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Enhanced scroll animations
    function initAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    entry.target.classList.add('visible');
                    
                    // Handle staggered animations for child elements
                    const staggeredElements = entry.target.querySelectorAll('.animate-up, .animate-text, .animate-card');
                    staggeredElements.forEach((el, index) => {
                        setTimeout(() => {
                            el.classList.add('visible');
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);
        
        // Observe all elements with animation classes
        const animatedElements = document.querySelectorAll('.fade-in, .animate-up, .animate-text, .animate-card, .animate-hero');
        animatedElements.forEach(el => {
            observer.observe(el);
        });
        
        // Initialize hero animations on page load
        setTimeout(() => {
            const heroElements = document.querySelectorAll('.animate-hero');
            heroElements.forEach((el, index) => {
                setTimeout(() => {
                    el.classList.add('visible');
                }, index * 200);
            });
        }, 300);
    }
    
    // Smooth scroll for anchor links
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href && href !== '#') {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    
                    if (target) {
                        const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                        
                        window.scrollTo({
                            top: offsetTop,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
    }
    
    // Form validation and enhancement
    function initFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                
                form.classList.add('was-validated');
                
                // Add loading state to submit button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn && form.checkValidity()) {
                    addLoadingState(submitBtn);
                }
            });
            
            // Real-time validation
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('blur', function() {
                    validateField(this);
                });
                
                input.addEventListener('input', function() {
                    if (this.classList.contains('is-invalid')) {
                        validateField(this);
                    }
                });
            });
        });
        
        // Price range slider functionality
        const priceSlider = document.getElementById('priceSlider');
        const priceRangeFill = document.getElementById('priceRangeFill');
        const currentPriceMin = document.getElementById('currentPriceMin');
        const currentPriceMax = document.getElementById('currentPriceMax');
        const resetPriceRange = document.getElementById('resetPriceRange');
        
        if (priceSlider) {
            const minPrice = parseFloat(priceSlider.min);
            const maxPrice = parseFloat(priceSlider.max);
            let currentMin = minPrice;
            let currentMax = maxPrice;
            
            // Update slider display
            function updateSliderDisplay() {
                const percentage = ((currentMax - minPrice) / (maxPrice - minPrice)) * 100;
                if (priceRangeFill) {
                    priceRangeFill.style.width = percentage + '%';
                }
                if (currentPriceMin) currentPriceMin.textContent = Math.round(currentMin);
                if (currentPriceMax) currentPriceMax.textContent = Math.round(currentMax);
            }
            
            // Initialize display
            updateSliderDisplay();
            
            // Handle slider input
            priceSlider.addEventListener('input', function() {
                currentMax = parseFloat(this.value);
                updateSliderDisplay();
                filterProducts();
            });
            
            // Reset price range
            if (resetPriceRange) {
                resetPriceRange.addEventListener('click', function() {
                    currentMin = minPrice;
                    currentMax = maxPrice;
                    priceSlider.value = maxPrice;
                    updateSliderDisplay();
                    filterProducts();
                });
            }
        }

        // Clear filters functionality
        const clearFiltersBtn = document.getElementById('clearFilters');
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', function() {
                // Reset search
                const searchInput = document.getElementById('productSearch');
                if (searchInput) {
                    searchInput.value = '';
                }
                
                // Reset price range slider
                if (priceSlider) {
                    const minPrice = parseFloat(priceSlider.min);
                    const maxPrice = parseFloat(priceSlider.max);
                    priceSlider.value = maxPrice;
                    if (priceRangeFill) priceRangeFill.style.width = '100%';
                    if (currentPriceMin) currentPriceMin.textContent = Math.round(minPrice);
                    if (currentPriceMax) currentPriceMax.textContent = Math.round(maxPrice);
                }
                
                // Reset all checkboxes
                const checkboxes = document.querySelectorAll('input[type="checkbox"][data-filter]');
                checkboxes.forEach(checkbox => {
                    if (checkbox.value === 'all') {
                        checkbox.checked = true;
                    } else {
                        checkbox.checked = false;
                    }
                });
                
                // Show all products
                const products = document.querySelectorAll('.product-item');
                products.forEach(product => {
                    product.classList.remove('hidden');
                });
                
                // Update no results message
                updateNoResultsMessage();
            });
        }
    }
    
    // Field validation
    function validateField(field) {
        const isValid = field.checkValidity();
        
        field.classList.remove('is-valid', 'is-invalid');
        field.classList.add(isValid ? 'is-valid' : 'is-invalid');
        
        // Show/hide custom error message
        const errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (errorElement) {
            if (!isValid) {
                errorElement.textContent = field.validationMessage;
                errorElement.style.display = 'block';
            } else {
                errorElement.style.display = 'none';
            }
        }
    }
    
    // Add loading state to button
    function addLoadingState(button) {
        const originalText = button.innerHTML;
        const spinner = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>';
        
        button.innerHTML = spinner + 'Processing...';
        button.disabled = true;
        
        // Remove loading state after form submission (or timeout)
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 3000);
    }
    
    // Utility function to show alerts
    window.showAlert = function(message, type = 'success') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
        alertContainer.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at top of main content
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.insertBefore(alertContainer, mainContent.firstChild);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (alertContainer.parentNode) {
                    alertContainer.remove();
                }
            }, 5000);
        }
    };
    
    // Handle AJAX errors
    window.handleAjaxError = function(xhr, status, error) {
        console.error('AJAX Error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
    };
    
    // Format currency
    window.formatCurrency = function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(amount);
    };
    
    // Format number with commas
    window.formatNumber = function(num) {
        return new Intl.NumberFormat('en-US').format(num);
    };
    
    // Product gallery functionality
    function initProductGallery() {
        // Add hover effects to thumbnails
        const thumbnails = document.querySelectorAll('.thumbnail-image');
        thumbnails.forEach(thumb => {
            thumb.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05)';
                this.style.transition = 'transform 0.2s ease';
            });
            
            thumb.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });
    }
    
    // Product filtering function
    function filterProducts() {
        const searchInput = document.getElementById('productSearch');
        const priceMinInput = document.getElementById('priceMin');
        const priceMaxInput = document.getElementById('priceMax');
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
        const priceMin = priceMinInput ? parseFloat(priceMinInput.value) || 0 : 0;
        const priceMax = priceMaxInput ? parseFloat(priceMaxInput.value) || Infinity : Infinity;
        
        // Get active filters
        const activeFilters = {};
        const filterCheckboxes = document.querySelectorAll('input[type="checkbox"][data-filter]:checked');
        
        filterCheckboxes.forEach(checkbox => {
            const filterName = checkbox.getAttribute('data-filter');
            const filterValue = checkbox.value;
            
            if (filterValue !== 'all') {
                if (!activeFilters[filterName]) {
                    activeFilters[filterName] = [];
                }
                activeFilters[filterName].push(filterValue);
            }
        });
        
        // Filter products
        const products = document.querySelectorAll('.product-item');
        let visibleCount = 0;
        
        products.forEach(product => {
            let shouldShow = true;
            
            // Search filter
            if (searchTerm) {
                const productName = product.querySelector('.product-name')?.textContent.toLowerCase() || '';
                const productDescription = product.querySelector('.product-description')?.textContent.toLowerCase() || '';
                const characteristics = Array.from(product.querySelectorAll('[data-characteristic]')).map(el => 
                    el.textContent.toLowerCase()
                ).join(' ');
                
                const searchableText = `${productName} ${productDescription} ${characteristics}`;
                if (!searchableText.includes(searchTerm)) {
                    shouldShow = false;
                }
            }
            
            // Price filter with slider
            const priceElement = product.querySelector('.product-price');
            if (priceElement && shouldShow) {
                const priceText = priceElement.textContent.replace(/[^\d.]/g, '');
                const price = parseFloat(priceText) || 0;
                
                // Get current slider values
                const slider = document.getElementById('priceSlider');
                if (slider) {
                    const minPrice = parseFloat(slider.min);
                    const maxPrice = parseFloat(slider.value);
                    
                    if (price < minPrice || price > maxPrice) {
                        shouldShow = false;
                    }
                }
            }
            
            // Characteristic filters
            if (shouldShow) {
                for (const [filterName, filterValues] of Object.entries(activeFilters)) {
                    const productCharacteristics = Array.from(product.querySelectorAll(`[data-characteristic="${filterName}"]`));
                    
                    if (productCharacteristics.length > 0) {
                        const hasMatchingCharacteristic = productCharacteristics.some(char => 
                            filterValues.includes(char.textContent.trim())
                        );
                        
                        if (!hasMatchingCharacteristic) {
                            shouldShow = false;
                            break;
                        }
                    }
                }
            }
            
            // Show/hide product
            if (shouldShow) {
                product.classList.remove('hidden');
                visibleCount++;
            } else {
                product.classList.add('hidden');
            }
        });
        
        // Update no results message
        updateNoResultsMessage();
    }
    
    // Update no results message
    function updateNoResultsMessage() {
        const activeTab = document.querySelector('.tab-pane.active');
        if (!activeTab) return;
        
        const products = activeTab.querySelectorAll('.product-item:not(.hidden)');
        const noResultsMessage = activeTab.querySelector('.no-results-message');
        
        if (products.length === 0) {
            if (!noResultsMessage) {
                const message = document.createElement('div');
                message.className = 'no-results-message text-center py-5';
                message.innerHTML = `
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">Товары не найдены</h5>
                    <p class="text-muted">Попробуйте изменить критерии поиска или фильтрации</p>
                `;
                activeTab.appendChild(message);
            }
        } else if (noResultsMessage) {
            noResultsMessage.remove();
        }
    }
});

// Product Gallery - Change main image function (global scope)
function changeMainImage(imageSrc) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.style.opacity = '0.5';
        setTimeout(() => {
            mainImage.src = imageSrc;
            mainImage.style.opacity = '1';
        }, 150);
    }
}

// Add CSS for scrolled navbar
const style = document.createElement('style');
style.textContent = `
    .navbar.scrolled {
        background-color: rgba(255, 255, 255, 0.98) !important;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
    }
    
    .fade-in {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s ease;
    }
    
    .fade-in.active {
        opacity: 1;
        transform: translateY(0);
    }
    
    /* Ensure animations work on page load */
    .animate-hero {
        opacity: 0;
        transform: translateY(60px);
        transition: all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .animate-hero.visible {
        opacity: 1;
        transform: translateY(0);
    }
    
    .invalid-feedback {
        display: none;
        width: 100%;
        margin-top: 0.25rem;
        font-size: 0.875rem;
        color: #dc3545;
    }
    
    .is-invalid ~ .invalid-feedback {
        display: block;
    }
`;
document.head.appendChild(style);
