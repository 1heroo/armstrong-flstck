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
