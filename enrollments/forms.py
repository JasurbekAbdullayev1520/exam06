from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'semester', 'enrolled_at']

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control','min': 1,'max': 12}),
            'enrolled_at': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            }

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        course = cleaned_data.get('course')

        if student and course:
            exists = Enrollment.objects.filter(
                student=student,
                course=course
            ).exists()

            if exists:
                raise forms.ValidationError(
                    "Bu student ushbu kursga allaqachon yozilgan."
                )

        return cleaned_data
