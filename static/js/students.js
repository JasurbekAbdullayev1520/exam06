// =====================================================
// Students Module JavaScript
// =====================================================

$(document).ready(function() {
    // Initialize student-specific functionality
    initStudentSearch();
    initStudentFilters();
    initStudentStats();
});

// Student Search
function initStudentSearch() {
    const searchInput = $('input[name="search"]');
    
    if (searchInput.length) {
        searchInput.on('input', debounce(function() {
            const value = $(this).val();
            
            if (value.length >= 2) {
                filterStudents(value);
            } else {
                $('table tbody tr').show();
            }
        }, 300));
    }
}

// Filter Students
function filterStudents(query) {
    query = query.toLowerCase();
    
    $('table tbody tr').each(function() {
        const text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(query));
    });
    
    updateResultsCount();
}

// Initialize Filters
function initStudentFilters() {
    $('select[name="gender"], select[name="ordering"]').on('change', function() {
        $('#searchForm').submit();
    });
}

// Update Results Count
function updateResultsCount() {
    const visibleRows = $('table tbody tr:visible').length;
    const totalRows = $('table tbody tr').length;
    
    if ($('.results-count').length === 0) {
        $('table').before(`<p class="results-count text-muted mb-2"></p>`);
    }
    
    $('.results-count').text(`${visibleRows} dan ${totalRows} ta natija ko'rsatilmoqda`);
}

// Student Statistics
function initStudentStats() {
    calculateAverageAge();
    calculateGenderDistribution();
}

// Calculate Average Age
function calculateAverageAge() {
    const birthDates = [];
    
    $('table tbody tr').each(function() {
        const dateText = $(this).find('td:eq(5)').text();
        if (dateText && dateText !== '-') {
            birthDates.push(new Date(dateText));
        }
    });
    
    if (birthDates.length > 0) {
        const today = new Date();
        const ages = birthDates.map(date => {
            const age = today.getFullYear() - date.getFullYear();
            return age;
        });
        
        const avgAge = ages.reduce((a, b) => a + b, 0) / ages.length;
        console.log('O\'rtacha yosh:', avgAge.toFixed(1));
    }
}

// Calculate Gender Distribution
function calculateGenderDistribution() {
    let maleCount = 0;
    let femaleCount = 0;
    
    $('.badge').each(function() {
        if ($(this).hasClass('bg-primary')) {
            maleCount++;
        } else if ($(this).hasClass('bg-danger')) {
            femaleCount++;
        }
    });
    
    console.log('Jins taqsimoti:', {
        erkak: maleCount,
        ayol: femaleCount
    });
}

// Export Students
function exportStudents() {
    showLoading();
    
    setTimeout(function() {
        exportTableToCSV('talabalar.csv');
        hideLoading();
        showToast('Talabalar eksport qilindi', 'success');
    }, 1000);
}

// Print Student List
function printStudents() {
    window.print();
}

// Bulk Actions
function selectAllStudents() {
    $('.student-checkbox').prop('checked', true);
    updateBulkActions();
}

function deselectAllStudents() {
    $('.student-checkbox').prop('checked', false);
    updateBulkActions();
}

function updateBulkActions() {
    const selectedCount = $('.student-checkbox:checked').length;
    
    if (selectedCount > 0) {
        $('.bulk-actions').show();
        $('.selected-count').text(selectedCount);
    } else {
        $('.bulk-actions').hide();
    }
}

// Delete Selected Students
function deleteSelectedStudents() {
    const selectedIds = [];
    
    $('.student-checkbox:checked').each(function() {
        selectedIds.push($(this).val());
    });
    
    if (selectedIds.length === 0) {
        showToast('Talabalarni tanlang', 'warning');
        return;
    }
    
    if (confirm(`${selectedIds.length} ta talabani o'chirmoqchimisiz?`)) {
        showLoading();
        
        // AJAX request to delete students
        $.ajax({
            url: '/students/bulk-delete/',
            method: 'POST',
            data: {
                student_ids: selectedIds,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                hideLoading();
                showToast('Talabalar o\'chirildi', 'success');
                location.reload();
            },
            error: function(xhr, status, error) {
                handleAjaxError(xhr, status, error);
            }
        });
    }
}

// Student Quick View Modal
function showStudentQuickView(studentId) {
    showLoading();
    
    $.ajax({
        url: `/students/${studentId}/quick-view/`,
        method: 'GET',
        success: function(data) {
            hideLoading();
            
            const modal = `
                <div class="modal fade" id="studentModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Talaba ma'lumotlari</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                ${data.html}
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            $('body').append(modal);
            const modalElement = new bootstrap.Modal(document.getElementById('studentModal'));
            modalElement.show();
            
            $('#studentModal').on('hidden.bs.modal', function() {
                $(this).remove();
            });
        },
        error: function(xhr, status, error) {
            handleAjaxError(xhr, status, error);
        }
    });
}

// Export to global scope
window.studentModule = {
    exportStudents,
    printStudents,
    selectAllStudents,
    deselectAllStudents,
    deleteSelectedStudents,
    showStudentQuickView
};
