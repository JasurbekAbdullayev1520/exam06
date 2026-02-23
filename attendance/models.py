from django.db import models
from apps.students.models import Student
from apps.courses.models import Group


class Lesson(models.Model):
    """Dars sessiyasi"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons', verbose_name="Guruh")
    date = models.DateField(verbose_name="Sana")
    topic = models.CharField(max_length=200, blank=True, verbose_name="Mavzu")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    created_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True,
        verbose_name="Kiritgan"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ['-date']
        unique_together = ['group', 'date']

    def __str__(self):
        return f"{self.group.name} - {self.date}"

    def get_attendance_rate(self):
        total = self.attendances.count()
        if total == 0:
            return 0
        present = self.attendances.filter(status='present').count()
        return round(present / total * 100, 1)


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Keldi'),
        ('absent', 'Kelmadi'),
        ('late', 'Kechikdi'),
        ('excused', 'Sababli'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendances', verbose_name="Dars")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances', verbose_name="Talaba")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='absent', verbose_name="Holat")
    notes = models.CharField(max_length=200, blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Davomat"
        verbose_name_plural = "Davomat"
        unique_together = ['lesson', 'student']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.lesson.date} - {self.get_status_display()}"