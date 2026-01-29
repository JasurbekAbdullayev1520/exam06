// =====================================================
// Student Management System - Main JavaScript
// =====================================================

// Document Ready
$(document).ready(function() {
    // Initialize tooltips
    initTooltips();
    
    // Initialize alerts auto-hide
    autoHideAlerts();
    
    // Initialize search functionality
    initSearch();
    
    // Initialize form validation
    initFormValidation();
    
    // Initialize animations
    initAnimations();
});

// Initialize Bootstrap Tooltips
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Auto-hide alerts after 5 seconds
function autoHideAlerts() {
    $('.alert').each(function() {
        const $alert = $(this);
        setTimeout(function() {
            $alert.fadeOut('slow', function() {
                $(this).remove();
            });
        }, 5000);
    });
}

// Initialize Search Functionality
function initSearch() {
    // Real-time search filter
    $('#searchInput').on('keyup', function() {
        const value = $(this).val().toLowerCase();
        
        $('table tbody tr').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
    
    // Search form submission
    $('#searchForm').on('submit', function(e) {
        const searchValue = $(this).find('input[name="search"]').val();
        if (searchValue.trim() === '') {
            e.preventDefault();
            window.location.href = window.location.pathname;
        }
    });
}

// Initialize Form Validation
function initFormValidation() {
    // Bootstrap form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Add 'form-control' class to all form inputs
    $('form input, form select, form textarea').addClass('form-control');
}

// Initialize Animations
function initAnimations() {
    // Fade in cards
    $('.card').each(function(i) {
        const $card = $(this);
        setTimeout(function() {
            $card.addClass('fade-in');
        }, i * 100);
    });
}

// Confirm Delete
function confirmDelete(message = 'Rostdan ham o\'chirmoqchimisiz?') {
    return confirm(message);
}

// Show Loading Spinner
function showLoading() {
    const spinner = `
        <div class="loading-overlay">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Yuklanmoqda...</span>
            </div>
        </div>
    `;
    $('body').append(spinner);
}

// Hide Loading Spinner
function hideLoading() {
    $('.loading-overlay').remove();
}

// Format Date
function formatDate(date) {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}.${month}.${year}`;
}

// Toast Notification
function showToast(message, type = 'info') {
    const toast = `
        <div class="toast-container position-fixed top-0 end-0 p-3">
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        </div>
    `;
    
    $('body').append(toast);
    const toastElement = new bootstrap.Toast($('.toast').last()[0]);
    toastElement.show();
    
    setTimeout(function() {
        $('.toast-container').remove();
    }, 5000);
}

// Export Table to CSV
function exportTableToCSV(filename = 'export.csv') {
    const csv = [];
    const rows = document.querySelectorAll('table tr');
    
    for (const row of rows) {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        
        for (const col of cols) {
            csvRow.push(col.innerText);
        }
        
        csv.push(csvRow.join(','));
    }
    
    downloadCSV(csv.join('\n'), filename);
}

// Download CSV
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Print Page
function printPage() {
    window.print();
}

// Copy to Clipboard
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    
    showToast('Nusxalandi!', 'success');
}

// Validate Email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate Phone Number
function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]+$/;
    return re.test(phone);
}

// Get URL Parameter
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

// Debounce Function
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

// Handle AJAX Errors
function handleAjaxError(xhr, status, error) {
    console.error('AJAX Error:', status, error);
    showToast('Xatolik yuz berdi. Qaytadan urinib ko\'ring.', 'danger');
    hideLoading();
}

// Loading Overlay CSS
const loadingStyles = `
    <style>
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
    </style>
`;
$('head').append(loadingStyles);

// Export functions to global scope
window.studentManagement = {
    confirmDelete,
    showLoading,
    hideLoading,
    formatDate,
    showToast,
    exportTableToCSV,
    printPage,
    copyToClipboard,
    validateEmail,
    validatePhone,
    getUrlParameter,
    debounce
};
