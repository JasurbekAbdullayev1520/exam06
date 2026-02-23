# students/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from datetime import date
from django.urls import reverse


class Student(models.Model):
    """
    Student model with comprehensive fields and validation
    """
    
    GENDER_CHOICES = [
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Faol'),
        ('inactive', 'Faol emas'),
        ('graduated', 'Bitirgan'),
        ('suspended', 'To\'xtatilgan'),
        ('dropped', 'Tashlab ketgan'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    # Basic Information
    student_id = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name='Talaba ID',
        help_text='Noyob talaba identifikatori'
    )
    
    first_name = models.CharField(
        max_length=100,
        verbose_name='Ism',
        db_index=True
    )
    
    last_name = models.CharField(
        max_length=100,
        verbose_name='Familiya',
        db_index=True
    )
    
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Otasining ismi'
    )
    
    # Contact Information
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        db_index=True
    )
    
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?998\d{9}$',
                message='Telefon raqami +998XXXXXXXXX formatida bo\'lishi kerak'
            )
        ],
        verbose_name='Telefon raqami',
        help_text='Format: +998901234567'
    )
    
    alternative_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Qo\'shimcha telefon'
    )
    
    telegram_username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Telegram username'
    )
    
    # Personal Information
    date_of_birth = models.DateField(
        verbose_name='Tug\'ilgan sana'
    )
    
    age = models.PositiveIntegerField(
        editable=False,
        verbose_name='Yosh',
        null=True,
        blank=True
    )
    
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Jins'
    )
    
    blood_type = models.CharField(
        max_length=3,
        choices=BLOOD_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Qon guruhi'
    )
    
    nationality = models.CharField(
        max_length=100,
        default='O\'zbekiston',
        verbose_name='Millati'
    )
    
    # Address Information
    address = models.TextField(
        verbose_name='Manzil'
    )
    
    city = models.CharField(
        max_length=100,
        verbose_name='Shahar',
        db_index=True
    )
    
    region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Viloyat'
    )
    
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Pochta indeksi'
    )
    
    # Guardian Information
    guardian_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Ota-ona/Vasiy ismi'
    )
    
    guardian_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Ota-ona telefoni'
    )
    
    guardian_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Ota-ona emaili'
    )
    
    guardian_relationship = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Qarindoshlik darajasi',
        help_text='Masalan: ota, ona, aka, opa'
    )
    
    # Education Information
    previous_school = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Oldingi o\'quv maskani'
    )
    
    education_level = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Ta\'lim darajasi',
        help_text='Masalan: O\'rta maktab, Kollej, Universitet'
    )
    
    # Status and Dates
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Holat',
        db_index=True
    )
    
    enrollment_date = models.DateField(
        default=timezone.now,
        verbose_name='Ro\'yxatdan o\'tgan sana'
    )
    
    graduation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Bitirgan sana'
    )
    
    # Financial Information
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Chegirma foizi'
    )
    
    # Additional Information
    profile_picture = models.ImageField(
        upload_to='students/profiles/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Profil rasmi'
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Qo\'shimcha ma\'lumotlar'
    )
    
    emergency_contact_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Favqulodda vaziyat uchun aloqa'
    )
    
    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Favqulodda aloqa telefoni'
    )
    
    # Medical Information
    medical_conditions = models.TextField(
        blank=True,
        null=True,
        verbose_name='Tibbiy ma\'lumotlar',
        help_text='Allergiya, kasalliklar va boshqalar'
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yangilangan vaqt'
    )
    
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_students',
        verbose_name='Kim tomonidan yaratilgan'
    )
    
    # Relationships
    courses = models.ManyToManyField(
        'courses.Course',
        through='enrollments.Enrollment',
        related_name='students',
        blank=True
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabalar'
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['email']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['status']),
            models.Index(fields=['city']),
            models.Index(fields=['enrollment_date']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def get_absolute_url(self):
        return reverse('students:student_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        # Auto-generate student_id if not provided
        if not self.student_id:
            self.student_id = self.generate_student_id()
        
        # Calculate age
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_student_id():
        """Generate unique student ID"""
        import random
        import string
        
        year = timezone.now().year
        
        # Get last student ID for this year
        last_student = Student.objects.filter(
            student_id__startswith=f'STD{year}'
        ).order_by('-student_id').first()
        
        if last_student:
            last_number = int(last_student.student_id[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f'STD{year}{new_number:04d}'
    
    def get_full_name(self):
        """Return full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        """Calculate and return age"""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def get_active_courses(self):
        """Get all active courses for this student"""
        from enrollments.models import Enrollment
        return Enrollment.objects.filter(
            student=self,
            status='active'
        ).select_related('course')
    
    def get_total_paid(self):
        """Get total amount paid by student"""
        from payments.models import Payment
        return Payment.objects.filter(
            student=self,
            status='completed'
        ).aggregate(models.Sum('paid_amount'))['paid_amount__sum'] or 0
    
    def get_total_debt(self):
        """Get total debt amount"""
        from payments.models import Payment
        payments = Payment.objects.filter(
            student=self,
            status__in=['pending', 'partial']
        )
        
        total_debt = sum([payment.debt for payment in payments])
        return total_debt
    
    def get_attendance_percentage(self):
        """Calculate overall attendance percentage"""
        from attendance.models import Attendance
        
        total = Attendance.objects.filter(student=self).count()
        if total == 0:
            return 0
        
        present = Attendance.objects.filter(
            student=self,
            status='present'
        ).count()
        
        return round((present / total) * 100, 2)
    
    def is_debtor(self):
        """Check if student has debt"""
        return self.get_total_debt() > 0
    
    def activate(self):
        """Activate student"""
        self.status = 'active'
        self.save()
    
    def deactivate(self):
        """Deactivate student"""
        self.status = 'inactive'
        self.save()
    
    def graduate(self):
        """Mark student as graduated"""
        self.status = 'graduated'
        self.graduation_date = timezone.now().date()
        self.save()
    
    def suspend(self):
        """Suspend student"""
        self.status = 'suspended'
        self.save()


class StudentDocument(models.Model):
    """Student documents model"""
    
    DOCUMENT_TYPE_CHOICES = [
        ('passport', 'Pasport'),
        ('birth_certificate', 'Tug\'ilganlik haqida guvohnoma'),
        ('photo', 'Fotosurat'),
        ('certificate', 'Sertifikat'),
        ('contract', 'Shartnoma'),
        ('other', 'Boshqa'),
    ]
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Talaba'
    )
    
    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name='Hujjat turi'
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name='Sarlavha'
    )
    
    file = models.FileField(
        upload_to='students/documents/%Y/%m/',
        verbose_name='Fayl'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Tavsif'
    )
    
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yuklangan vaqt'
    )
    
    uploaded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_student_documents',
        verbose_name='Kim yukladi'
    )
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Talaba hujjati'
        verbose_name_plural = 'Talaba hujjatlari'
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.title}"