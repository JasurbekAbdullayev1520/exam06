// =====================================================
// Courses Module JavaScript
// =====================================================

$(document).ready(function() {
    // Initialize course-specific functionality
    initCourseFilters();
    initCourseCards();
    initCourseStats();
});

// Course Filters
function initCourseFilters() {
    $('select[name="semester"], select[name="ordering"]').on('change', function() {
        $(this).closest('form').submit();
    });
    
    // Real-time search
    $('input[name="search"]').on('input', debounce(function() {
        filterCourses($(this).val());
    }, 300));
}

// Filter Courses
function filterCourses(query) {
    query = query.toLowerCase();
    
    $('.course-card').each(function() {
        const title = $(this).find('h5').text().toLowerCase();
        const code = $(this).find('small').text().toLowerCase();
        
        if (title.includes(query) || code.includes(query)) {
            $(this).closest('.col-md-6, .col-lg-4').show();
        } else {
            $(this).closest('.col-md-6, .col-lg-4').hide();
        }
    });
    
    updateCourseCount();
}

// Update Course Count
function updateCourseCount() {
    const visible = $('.course-card:visible').length;
    const total = $('.course-card').length;
    
    if ($('.course-count').length === 0) {
        $('.row.g-4').before(`<p class="course-count text-muted mb-3"></p>`);
    }
    
    $('.course-count').text(`${visible} dan ${total} ta kurs ko'rsatilmoqda`);
}

// Course Cards Animation
function initCourseCards() {
    $('.course-card').each(function(i) {
        const $card = $(this);
        setTimeout(function() {
            $card.addClass('fade-in');
        }, i * 100);
    });
    
    // Hover effects
    $('.course-card').hover(
        function() {
            $(this).find('.card-footer').addClass('bg-light');
        },
        function() {
            $(this).find('.card-footer').removeClass('bg-light');
        }
    );
}

// Course Statistics
function initCourseStats() {
    calculateTotalCredits();
    calculateAverageEnrollment();
}

// Calculate Total Credits
function calculateTotalCredits() {
    let totalCredits = 0;
    
    $('.course-card').each(function() {
        const credits = parseInt($(this).find('.badge.bg-light').text());
        if (!isNaN(credits)) {
            totalCredits += credits;
        }
    });
    
    console.log('Jami kreditlar:', totalCredits);
}

// Calculate Average Enrollment
function calculateAverageEnrollment() {
    let totalEnrollments = 0;
    let courseCount = 0;
    
    $('.badge.bg-secondary').each(function() {
        const enrollment = parseInt($(this).text());
        if (!isNaN(enrollment)) {
            totalEnrollments += enrollment;
            courseCount++;
        }
    });
    
    if (courseCount > 0) {
        const avgEnrollment = totalEnrollments / courseCount;
        console.log('O\'rtacha talabalar soni:', avgEnrollment.toFixed(1));
    }
}

// Export Courses
function exportCourses() {
    showLoading();
    
    const courses = [];
    
    $('.course-card').each(function() {
        const name = $(this).find('h5').text();
        const code = $(this).find('small').first().text();
        const credits = $(this).find('.badge.bg-light').text();
        const instructor = $(this).find('.info-item:first span').text();
        const semester = $(this).find('.badge.bg-info').text();
        const students = $(this).find('.badge.bg-secondary').text();
        
        courses.push({
            name,
            code,
            credits,
            instructor,
            semester,
            students
        });
    });
    
    // Convert to CSV
    let csv = 'Nom,Kod,Kredit,O\'qituvchi,Semestr,Talabalar\n';
    courses.forEach(course => {
        csv += `"${course.name}","${course.code}","${course.credits}","${course.instructor}","${course.semester}","${course.students}"\n`;
    });
    
    downloadCSV(csv, 'kurslar.csv');
    hideLoading();
    showToast('Kurslar eksport qilindi', 'success');
}

// Course Detail - Student Filter
function filterStudentsByStatus(status) {
    $('tbody tr').each(function() {
        if (status === 'all') {
            $(this).show();
        } else {
            const rowStatus = $(this).data('status');
            $(this).toggle(rowStatus === status);
        }
    });
    
    updateStudentCount(status);
}

// Update Student Count
function updateStudentCount(status) {
    const visible = $('tbody tr:visible').length;
    
    if ($('.student-count').length === 0) {
        $('table').before(`<p class="student-count text-muted mb-2"></p>`);
    }
    
    const statusText = status === 'all' ? 'barcha' : status;
    $('.student-count').text(`${visible} ta ${statusText} talaba`);
}

// Add Student to Course Modal
function showAddStudentModal(courseId) {
    const modal = `
        <div class="modal fade" id="addStudentModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Talaba qo'shish</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="addStudentForm">
                            <div class="mb-3">
                                <label class="form-label">Talaba</label>
                                <select class="form-select" name="student_id" required>
                                    <option value="">Tanlang...</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Semestr</label>
                                <input type="number" class="form-control" name="semester" min="1" max="8" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Bekor qilish</button>
                        <button type="button" class="btn btn-primary" onclick="submitAddStudent(${courseId})">Qo'shish</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    $('body').append(modal);
    const modalElement = new bootstrap.Modal(document.getElementById('addStudentModal'));
    modalElement.show();
    
    // Load students
    loadAvailableStudents(courseId);
    
    $('#addStudentModal').on('hidden.bs.modal', function() {
        $(this).remove();
    });
}

// Load Available Students
function loadAvailableStudents(courseId) {
    $.ajax({
        url: `/courses/${courseId}/available-students/`,
        method: 'GET',
        success: function(data) {
            const select = $('#addStudentForm select[name="student_id"]');
            data.students.forEach(student => {
                select.append(`<option value="${student.id}">${student.name}</option>`);
            });
        },
        error: function(xhr, status, error) {
            handleAjaxError(xhr, status, error);
        }
    });
}

// Submit Add Student
function submitAddStudent(courseId) {
    const form = $('#addStudentForm');
    const studentId = form.find('[name="student_id"]').val();
    const semester = form.find('[name="semester"]').val();
    
    if (!studentId || !semester) {
        showToast('Barcha maydonlarni to\'ldiring', 'warning');
        return;
    }
    
    showLoading();
    
    $.ajax({
        url: '/enrollments/create/',
        method: 'POST',
        data: {
            student: studentId,
            course: courseId,
            semester: semester,
            status: 'active',
            csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            hideLoading();
            $('#addStudentModal').modal('hide');
            showToast('Talaba qo\'shildi', 'success');
            location.reload();
        },
        error: function(xhr, status, error) {
            handleAjaxError(xhr, status, error);
        }
    });
}

// Course Analytics
function showCourseAnalytics(courseId) {
    showLoading();
    
    $.ajax({
        url: `/courses/${courseId}/analytics/`,
        method: 'GET',
        success: function(data) {
            hideLoading();
            displayAnalyticsChart(data);
        },
        error: function(xhr, status, error) {
            handleAjaxError(xhr, status, error);
        }
    });
}

// Display Analytics Chart
function displayAnalyticsChart(data) {
    // Implementation would use Chart.js or similar library
    console.log('Course Analytics:', data);
}

// Export to global scope
window.courseModule = {
    exportCourses,
    filterStudentsByStatus,
    showAddStudentModal,
    showCourseAnalytics
};
