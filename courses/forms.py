from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','code', 'description', 'oylik_tolov', 'kurs_davomiligi', 'year']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CS101','id': 'id_code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'oylik_tolov': forms.NumberInput(attrs={'class': 'form-control'}),
            'kurs_davomiligi': forms.NumberInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }