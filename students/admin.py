# students/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import Student, StudentDocument


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Professional admin interface for Student model
    """
    
    list_display = [
        'student_id_display',
        'full_name_display',
        'email',
        'phone_number',
        'city',
        'status_badge',
        'age',
        'enrollment_date',
        'courses_count',
        'actions_display'
    ]
    
    list_filter = [
        'status',
        'gender',
        'city',
        'enrollment_date',
        'created_at',
    ]
    
    search_fields = [
        'student_id',
        'first_name',
        'last_name',
        'email',
        'phone_number',
    ]
    
    readonly_fields = [
        'student_id',
        'age',
        'created_at',
        'updated_at',
        'created_by',
    ]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': (
                'student_id',
                ('first_name', 'last_name', 'middle_name'),
                'profile_picture',
            )
        }),
        ('Aloqa ma\'lumotlari', {
            'fields': (
                ('email', 'phone_number'),
                ('alternative_phone', 'telegram_username'),
            )
        }),
        ('Shaxsiy ma\'lumotlar', {
            'fields': (
                ('date_of_birth', 'age', 'gender'),
                ('blood_type', 'nationality'),
            )
        }),
        ('Manzil', {
            'fields': (
                'address',
                ('city', 'region', 'postal_code'),
            )
        }),
        ('Vasiy ma\'lumotlari', {
            'fields': (
                ('guardian_name', 'guardian_relationship'),
                ('guardian_phone', 'guardian_email'),
            ),
            'classes': ('collapse',)
        }),
        ('Ta\'lim ma\'lumotlari', {
            'fields': (
                ('previous_school', 'education_level'),
            ),
            'classes': ('collapse',)
        }),
        ('Holat va sanalar', {
            'fields': (
                ('status', 'discount_percentage'),
                ('enrollment_date', 'graduation_date'),
            )
        }),
        ('Qo\'shimcha', {
            'fields': (
                'notes',
                ('emergency_contact_name', 'emergency_contact_phone'),
                'medical_conditions',
            ),
            'classes': ('collapse',)
        }),
        ('Tizim ma\'lumotlari', {
            'fields': (
                ('created_at', 'updated_at'),
                'created_by',
            ),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'enrollment_date'
    ordering = ['-created_at']
    
    actions = [
        'activate_students',
        'deactivate_students',
        'mark_as_graduated',
        'export_to_excel',
    ]
    
    def student_id_display(self, obj):
        """Display student ID as link"""
        url = reverse('admin:students_student_change', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.student_id)
    student_id_display.short_description = 'ID'
    
    def full_name_display(self, obj):
        """Display full name with avatar"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="30" height="30" style="border-radius: 50%;" /> {}',
                obj.profile_picture.url,
                obj.get_full_name()
            )
        return obj.get_full_name()
    full_name_display.short_description = 'To\'liq ismi'
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'active': 'success',
            'inactive': 'secondary',
            'graduated': 'primary',
            'suspended': 'warning',
            'dropped': 'danger',
        }
        color = colors.get(obj.status, 'secondary')
        
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Holat'
    
    def courses_count(self, obj):
        """Display number of courses"""
        count = obj.courses.count()
        return format_html(
            '<span class="badge badge-info">{}</span>',
            count
        )
    courses_count.short_description = 'Kurslar'
    
    def actions_display(self, obj):
        """Display action buttons"""
        detail_url = reverse('students:student_detail', args=[obj.pk])
        return format_html(
            '<a href="{}" class="button" target="_blank">Ko\'rish</a>',
            detail_url
        )
    actions_display.short_description = 'Harakatlar'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        qs = qs.select_related('created_by')
        qs = qs.prefetch_related('courses', 'documents')
        qs = qs.annotate(courses_count=Count('courses'))
        return qs
    
    def save_model(self, request, obj, form, change):
        """Save with created_by"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    # Actions
    def activate_students(self, request, queryset):
        """Activate selected students"""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} ta talaba faollashtirildi.')
    activate_students.short_description = 'Tanlangan talabalarni faollashtirish'
    
    def deactivate_students(self, request, queryset):
        """Deactivate selected students"""
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated} ta talaba faolsizlantirildi.')
    deactivate_students.short_description = 'Tanlangan talabalarni faolsizlantirish'
    
    def mark_as_graduated(self, request, queryset):
        """Mark students as graduated"""
        from django.utils import timezone
        updated = queryset.update(
            status='graduated',
            graduation_date=timezone.now().date()
        )
        self.message_user(request, f'{updated} ta talaba bitirgan deb belgilandi.')
    mark_as_graduated.short_description = 'Bitirgan deb belgilash'
    
    def export_to_excel(self, request, queryset):
        """Export to Excel"""
        # Implementation would redirect to export view
        from django.shortcuts import redirect
        ids = ','.join(str(obj.id) for obj in queryset)
        return redirect(f'/students/export/excel/?ids={ids}')
    export_to_excel.short_description = 'Excel ga eksport qilish'


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    """
    Admin interface for Student Documents
    """
    
    list_display = [
        'title',
        'student',
        'document_type',
        'file_link',
        'uploaded_by',
        'uploaded_at',
    ]
    
    list_filter = [
        'document_type',
        'uploaded_at',
    ]
    
    search_fields = [
        'title',
        'student__first_name',
        'student__last_name',
        'student__student_id',
    ]
    
    readonly_fields = [
        'uploaded_at',
        'uploaded_by',
    ]
    
    fieldsets = (
        ('Hujjat ma\'lumotlari', {
            'fields': (
                'student',
                'document_type',
                'title',
                'file',
                'description',
            )
        }),
        ('Tizim ma\'lumotlari', {
            'fields': (
                'uploaded_at',
                'uploaded_by',
            )
        }),
    )
    
    def file_link(self, obj):
        """Display file as link"""
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">Yuklab olish</a>',
                obj.file.url
            )
        return '-'
    file_link.short_description = 'Fayl'
    
    def save_model(self, request, obj, form, change):
        """Save with uploaded_by"""
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


# Custom Admin Site Configuration
admin.site.site_header = 'Talabalar Boshqaruv Tizimi'
admin.site.site_title = 'Admin Panel'
admin.site.index_title = 'Bosh sahifa'