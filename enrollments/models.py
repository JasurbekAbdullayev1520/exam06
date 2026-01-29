from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from students.models import Student
from courses.models import Course
from django.utils import timezone


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.BigIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(12),
        ]
    )
    enrolled_at = models.DateTimeField()
    
    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student}  {self.course}"

