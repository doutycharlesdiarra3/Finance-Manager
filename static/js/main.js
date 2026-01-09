// Finance Manager - Main JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .stat-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Number formatting for amount inputs
    const amountInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    amountInputs.forEach(input => {
        input.addEventListener('blur', function () {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // Dynamic category filtering based on transaction type
    const typeSelect = document.querySelector('select[name="type"]');
    const categorySelect = document.querySelector('select[name="category"]');

    if (typeSelect && categorySelect) {
        const allOptions = Array.from(categorySelect.options);

        typeSelect.addEventListener('change', function () {
            const selectedType = this.value;

            // Remove all options except the first (empty) one
            while (categorySelect.options.length > 1) {
                categorySelect.remove(1);
            }

            // Add back only matching options
            allOptions.forEach(option => {
                if (option.value === '') {
                    return; // Skip empty option
                }

                // This is a simple check - in production you'd want to store
                // the category type as a data attribute
                categorySelect.add(option.cloneNode(true));
            });
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading state to buttons on form submit
    forms.forEach(form => {
        form.addEventListener('submit', function () {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Chargement...';
            }
        });
    });

    // Tooltip initialization (if using Bootstrap tooltips)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add hover effect to table rows
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function () {
            this.style.cursor = 'pointer';
        });
    });

    // Confirm delete actions
    const deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(link => {
        if (!link.closest('form')) { // Only for links, not form buttons
            link.addEventListener('click', function (e) {
                if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
                    e.preventDefault();
                }
            });
        }
    });

    // Format currency values
    function formatCurrency(value) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(value);
    }

    // Add real-time amount preview
    const amountPreviewInputs = document.querySelectorAll('input[name="amount"]');
    amountPreviewInputs.forEach(input => {
        const preview = document.createElement('small');
        preview.className = 'text-muted d-block mt-1';
        input.parentElement.appendChild(preview);

        input.addEventListener('input', function () {
            if (this.value) {
                preview.textContent = `Aperçu: ${formatCurrency(this.value)}`;
            } else {
                preview.textContent = '';
            }
        });
    });

    console.log('Finance Manager initialized successfully!');
});

// Chart.js default configuration
if (typeof Chart !== 'undefined') {
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.color = '#6b7280';
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.legend.labels.padding = 15;
}
