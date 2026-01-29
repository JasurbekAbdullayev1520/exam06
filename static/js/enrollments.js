// =====================================================
// Enrollments Module JavaScript
// =====================================================

$(document).ready(function() {
    // Initialize enrollment-specific functionality
    initEnrollmentFilters();
    initEnrollmentForm();
    initGradeCalculations();
});

// Enrollment Filters
function initEnrollmentFilters() {
    $('select[name="student"], select[name="course"], select[name="status"], select[name="semester"]').on('change', function() {
        $(this).closest('form').submit();
    });
}

// Enrollment Form
function initEnrollmentForm() {
    const form = $('#enrollmentForm');
    
    if (form.length) {
        // Student selection change
        form.find('select[name="student"]').on('change', function() {
            const studentId = $(this).val();
            if (studentId) {
                loadStudentInfo(studentId);
            }
        });
        
        // Course selection change
        form.find('select[name="course"]').on('change', function() {
            const courseId = $(this).val();
            if (courseId) {
                loadCourseInfo(courseId);
            }
        });
        
        // Grade input validation
        form.find('input[name="grade"]').on('input', function() {
            validateGrade($(this));
        });
    }
}

// Load Student Info
function loadStudentInfo(studentId) {
    $.ajax({
        url: `/students/${studentId}/info/`,
        method: 'GET',
        success: function(data) {
            displayStudentInfo(data);
        },
        error: function(xhr, status, error) {
            console.error('Error loading student info:', error);
        }
    });
}

// Display Student Info
function displayStudentInfo(data) {
    if ($('.student-info').length === 0) {
        $('#enrollmentForm').prepend(`
            <div class="alert alert-info student-info">
                <h6>Talaba ma'lumotlari</h6>
                <div class="info-content"></div>
            </div>
        `);
    }
    
    $('.student-info .info-content').html(`
        <p class="mb-1"><strong>Ism:</strong> ${data.name}</p>
        <p class="mb-1"><strong>Email:</strong> ${data.email}</p>
        <p class="mb-0"><strong>Joriy kurslar:</strong> ${data.current_courses}</p>
    `);
}

// Load Course Info
function loadCourseInfo(courseId) {
    $.ajax({
        url: `/courses/${courseId}/info/`,
        method: 'GET',
        success: function(data) {
            displayCourseInfo(data);
        },
        error: function(xhr, status, error) {
            console.error('Error loading course info:', error);
        }
    });
}

// Display Course Info
function displayCourseInfo(data) {
    if ($('.course-info').length === 0) {
        $('#enrollmentForm').prepend(`
            <div class="alert alert-success course-info">
                <h6>Kurs ma'lumotlari</h6>
                <div class="info-content"></div>
            </div>
        `);
    }
    
    $('.course-info .info-content').html(`
        <p class="mb-1"><strong>Nom:</strong> ${data.name}</p>
        <p class="mb-1"><strong>Kod:</strong> ${data.code}</p>
        <p class="mb-1"><strong>Kredit:</strong> ${data.credits}</p>
        <p class="mb-0"><strong>Talabalar soni:</strong> ${data.enrollment_count}</p>
    `);
}

// Validate Grade
function validateGrade(input) {
    const value = parseInt(input.val());
    
    if (isNaN(value) || value < 0 || value > 100) {
        input.addClass('is-invalid');
        
        if (input.next('.invalid-feedback').length === 0) {
            input.after('<div class="invalid-feedback">0-100 oralig\'ida bo\'lishi kerak</div>');
        }
    } else {
        input.removeClass('is-invalid');
        input.next('.invalid-feedback').remove();
        
        // Show grade status
        updateGradeStatus(value, input);
    }
}

// Update Grade Status
function updateGradeStatus(grade, input) {
    let status = '';
    let className = '';
    
    if (grade >= 86) {
        status = 'A\'lo';
        className = 'success';
    } else if (grade >= 71) {
        status = 'Yaxshi';
        className = 'primary';
    } else if (grade >= 55) {
        status = 'Qoniqarli';
        className = 'warning';
    } else {
        status = 'Qoniqarsiz';
        className = 'danger';
    }
    
    if ($('.grade-status').length === 0) {
        input.after(`<div class="grade-status mt-2"></div>`);
    }
    
    $('.grade-status').html(`
        <span class="badge bg-${className}">${status} (${grade})</span>
    `);
}

// Grade Calculations
function initGradeCalculations() {
    calculateGradeDistribution();
}

// Calculate Grade Distribution
function calculateGradeDistribution() {
    const grades = {
        excellent: 0,  // 86-100
        good: 0,       // 71-85
        satisfactory: 0, // 55-70
        unsatisfactory: 0 // 0-54
    };
    
    $('.badge').each(function() {
        const text = $(this).text().trim();
        const grade = parseInt(text);
        
        if (!isNaN(grade)) {
            if (grade >= 86) {
                grades.excellent++;
            } else if (grade >= 71) {
                grades.good++;
            } else if (grade >= 55) {
                grades.satisfactory++;
            } else {
                grades.unsatisfactory++;
            }
        }
    });
    
    console.log('Baholar taqsimoti:', grades);
    return grades;
}

// Export Enrollments
function exportEnrollments() {
    showLoading();
    
    const enrollments = [];
    
    $('table tbody tr').each(function() {
        const id = $(this).find('td:eq(0)').text();
        const student = $(this).find('td:eq(1) .fw-bold').text();
        const course = $(this).find('td:eq(2) .fw-bold').text();
        const semester = $(this).find('td:eq(3) .badge').text();
        const grade = $(this).find('td:eq(4) .badge').text();
        const status = $(this).find('td:eq(5) .badge').text();
        const date = $(this).find('td:eq(6)').text();
        
        enrollments.push({
            id, student, course, semester, grade, status, date
        });
    });
    
    // Convert to CSV
    let csv = 'ID,Talaba,Kurs,Semestr,Baho,Holat,Sana\n';
    enrollments.forEach(enrollment => {
        csv += `"${enrollment.id}","${enrollment.student}","${enrollment.course}","${enrollment.semester}","${enrollment.grade}","${enrollment.status}","${enrollment.date}"\n`;
    });
    
    downloadCSV(csv, 'royxatlar.csv');
    hideLoading();
    showToast('Ro\'yxatlar eksport qilindi', 'success');
}

// Bulk Grade Update
function showBulkGradeUpdate() {
    const modal = `
        <div class="modal fade" id="bulkGradeModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Ommaviy baho yangilash</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="bulkGradeForm">
                            <div class="mb-3">
                                <label class="form-label">Kurs</label>
                                <select class="form-select" name="course_id" required>
                                    <option value="">Tanlang...</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Baho</label>
                                <input type="number" class="form-control" name="grade" min="0" max="100" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bekor qilish</button>
                        <button type="button" class="btn btn-primary" onclick="submitBulkGrade()">Yangilash</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    $('body').append(modal);
    const modalElement = new bootstrap.Modal(document.getElementById('bulkGradeModal'));
    modalElement.show();
    
    $('#bulkGradeModal').on('hidden.bs.modal', function() {
        $(this).remove();
    });
}

// Submit Bulk Grade
function submitBulkGrade() {
    const form = $('#bulkGradeForm');
    const courseId = form.find('[name="course_id"]').val();
    const grade = form.find('[name="grade"]').val();
    
    if (!courseId || !grade) {
        showToast('Barcha maydonlarni to\'ldiring', 'warning');
        return;
    }
    
    showLoading();
    
    $.ajax({
        url: '/enrollments/bulk-grade-update/',
        method: 'POST',
        data: {
            course_id: courseId,
            grade: grade,
            csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            hideLoading();
            $('#bulkGradeModal').modal('hide');
            showToast('Baholar yangilandi', 'success');
            location.reload();
        },
        error: function(xhr, status, error) {
            handleAjaxError(xhr, status, error);
        }
    });
}

// Generate Report
function generateEnrollmentReport() {
    showLoading();
    
    const filters = {
        student: $('select[name="student"]').val(),
        course: $('select[name="course"]').val(),
        status: $('select[name="status"]').val(),
        semester: $('select[name="semester"]').val()
    };
    
    $.ajax({
        url: '/enrollments/report/',
        method: 'GET',
        data: filters,
        success: function(data) {
            hideLoading();
            displayReport(data);
        },
        error: function(xhr, status, error) {
            handleAjaxError(xhr, status, error);
        }
    });
}

// Display Report
function displayReport(data) {
    console.log('Enrollment Report:', data);
    // Implementation would create a detailed report view
}

// Export to global scope
window.enrollmentModule = {
    exportEnrollments,
    showBulkGradeUpdate,
    generateEnrollmentReport
};
