// =====================================================
// Form Validation JavaScript - TUZATILGAN VERSIYA
// =====================================================

$(document).ready(function() {
    initFormValidation();
    initDatePickers();
    initPhoneValidation();
});

function initFormValidation() {
    // Bootstrap klasslarini qo'shish
    $('form input, form select, form textarea').addClass('form-control');
    
    // Formani yuborish qismi
    $('#studentForm').on('submit', function(e) {
        let isValid = true;
        
        // Faqat ko'rinadigan va required bo'lgan maydonlarni tekshiramiz
        $(this).find('[required]:visible').each(function() {
            if (!validateField($(this))) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault(); // Faqat xato bo'lsagina to'xtatamiz
            alert('Iltimos, barcha maydonlarni to\'g\'ri to\'ldiring');
        }
    });
}

function validateField(field) {
    const value = field.val() ? field.val().trim() : '';
    const fieldName = field.attr('name');
    
    field.removeClass('is-invalid is-valid');
    field.next('.invalid-feedback').remove();
    
    if (field.prop('required') && value === '') {
        showFieldError(field, 'Bu maydon to\'ldirilishi shart');
        return false;
    }

    // Yoshi bo'yicha cheklovni tekshiramiz (yosh > 0 bo'lishi kifoya)
    if (fieldName === 'date_of_birth' && value !== '') {
        const today = new Date();
        const birthDate = new Date(value);
        if (birthDate >= today) {
            showFieldError(field, 'Tug\'ilgan sana kelajakda bo\'lishi mumkin emas');
            return false;
        }
    }
    
    field.addClass('is-valid');
    return true;
}

function showFieldError(field, message) {
    field.addClass('is-invalid');
    if (field.next('.invalid-feedback').length === 0) {
        field.after(`<div class="invalid-feedback d-block">${message}</div>`);
    }
}

function initDatePickers() {
    // Bugungi sanadan oshib ketmasligini ta'minlaymiz
    const today = new Date().toISOString().split('T')[0];
    $('input[name="date_of_birth"]').attr('max', today);
}

function initPhoneValidation() {
    $('input[name="phone_number"]').on('input', function() {
        let value = $(this).val().replace(/[^\d\+\s\-\(\)]/g, '');
        $(this).val(value);
    });
}