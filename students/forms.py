# students/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Student, StudentDocument
from datetime import date, timedelta


class StudentForm(forms.ModelForm):
    """
    Main student form with comprehensive validation
    """
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'middle_name',
            'email', 'phone_number', 'alternative_phone', 'telegram_username',
            'date_of_birth', 'gender', 'blood_type', 'nationality',
            'address', 'city', 'region', 'postal_code',
            'guardian_name', 'guardian_phone', 'guardian_email', 'guardian_relationship',
            'previous_school', 'education_level',
            'status', 'enrollment_date', 'discount_percentage',
            'profile_picture', 'notes',
            'emergency_contact_name', 'emergency_contact_phone',
            'medical_conditions',
        ]
        
        widgets = {
            # Basic Info
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismni kiriting',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiyani kiriting',
                'required': True
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Otasining ismini kiriting'
            }),
            
            # Contact
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567',
                'required': True
            }),
            'alternative_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567'
            }),
            'telegram_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username'
            }),
            
            # Personal
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'blood_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            
            # Address
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'To\'liq manzilni kiriting',
                'required': True
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Shahar',
                'required': True
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Viloyat'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '100000'
            }),
            
            # Guardian
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ota-ona/Vasiy ismi'
            }),
            'guardian_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567'
            }),
            'guardian_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'guardian@email.com'
            }),
            'guardian_relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masalan: ota, ona, aka'
            }),
            
            # Education
            'previous_school': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Oldingi o\'quv maskani'
            }),
            'education_level': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masalan: O\'rta maktab'
            }),
            
            # Status
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'enrollment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'discount_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 0.01
            }),
            
            # Additional
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Qo\'shimcha ma\'lumotlar'
            }),
            
            # Emergency
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Favqulodda aloqa ismi'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567'
            }),
            
            # Medical
            'medical_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tibbiy ma\'lumotlar (allergiya, kasalliklar)'
            }),
        }
    
    def clean_date_of_birth(self):
        """Validate date of birth"""
        dob = self.cleaned_data.get('date_of_birth')
        
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            # Minimum age: 5 years
            if age < 5:
                raise ValidationError('Talaba kamida 5 yoshda bo\'lishi kerak')
            
            # Maximum age: 80 years
            if age > 80:
                raise ValidationError('Tug\'ilgan sana noto\'g\'ri')
            
            # Cannot be in the future
            if dob > today:
                raise ValidationError('Tug\'ilgan sana kelajakda bo\'lishi mumkin emas')
        
        return dob
    
    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        
        if email:
            # Check if email exists for other students
            qs = Student.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise ValidationError('Bu email allaqachon ishlatilmoqda')
        
        return email
    
    def clean_phone_number(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('phone_number')
        
        if phone:
            # Remove spaces and dashes
            phone = phone.replace(' ', '').replace('-', '')
            
            # Check format
            if not phone.startswith('+998'):
                raise ValidationError('Telefon raqami +998 bilan boshlanishi kerak')
            
            if len(phone) != 13:
                raise ValidationError('Telefon raqami 13 ta belgidan iborat bo\'lishi kerak')
        
        return phone
    
    def clean_discount_percentage(self):
        """Validate discount percentage"""
        discount = self.cleaned_data.get('discount_percentage')
        
        if discount:
            if discount < 0 or discount > 100:
                raise ValidationError('Chegirma 0 dan 100 gacha bo\'lishi kerak')
        
        return discount
    
    def clean(self):
        """Additional validation"""
        cleaned_data = super().clean()
        
        # Validate guardian info for minors
        dob = cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            if age < 18:
                if not cleaned_data.get('guardian_name'):
                    self.add_error('guardian_name', '18 yoshdan kichik talabalar uchun vasiy ma\'lumoti majburiy')
                
                if not cleaned_data.get('guardian_phone'):
                    self.add_error('guardian_phone', '18 yoshdan kichik talabalar uchun vasiy telefoni majburiy')
        
        return cleaned_data


class StudentSearchForm(forms.Form):
    """Search and filter form for students"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ism, familiya, email yoki ID bo\'yicha qidirish...'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Barcha holatlar')] + Student.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    gender = forms.ChoiceField(
        required=False,
        choices=[('', 'Barcha jinslar')] + Student.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Shahar'
        })
    )
    
    enrollment_date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    enrollment_date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    ordering = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Saralash'),
            ('first_name', 'Ism (A-Z)'),
            ('-first_name', 'Ism (Z-A)'),
            ('student_id', 'ID (o\'sish)'),
            ('-student_id', 'ID (kamayish)'),
            ('-enrollment_date', 'Yangi'),
            ('enrollment_date', 'Eski'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class StudentDocumentForm(forms.ModelForm):
    """Form for uploading student documents"""
    
    class Meta:
        model = StudentDocument
        fields = ['document_type', 'title', 'file', 'description']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hujjat nomi'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Hujjat haqida qo\'shimcha ma\'lumot'
            }),
        }
    
    def clean_file(self):
        """Validate file size and type"""
        file = self.cleaned_data.get('file')
        
        if file:
            # Check file size (max 5MB)
            if file.size > 5 * 1024 * 1024:
                raise ValidationError('Fayl hajmi 5MB dan oshmasligi kerak')
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png']
            file_extension = file.name.lower().split('.')[-1]
            
            if f'.{file_extension}' not in allowed_extensions:
                raise ValidationError(
                    f'Faqat quyidagi formatlar ruxsat etilgan: {", ".join(allowed_extensions)}'
                )
        
        return file


class BulkActionForm(forms.Form):
    """Form for bulk actions on students"""
    
    ACTION_CHOICES = [
        ('', 'Harakatni tanlang'),
        ('activate', 'Faollashtirish'),
        ('deactivate', 'Faolsizlantirish'),
        ('delete', 'O\'chirish'),
        ('export', 'Excel ga eksport'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    selected_students = forms.CharField(
        widget=forms.HiddenInput()
    )