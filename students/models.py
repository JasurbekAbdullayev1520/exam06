from django.db import models
from courses.models import Course

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True) 
    date_of_birth = models.DateField(null=True, blank=True) 
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True) 
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    courses = models.ManyToManyField(Course, related_name='students', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
