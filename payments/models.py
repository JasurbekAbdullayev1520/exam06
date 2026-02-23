from django.db import models
from apps.students.models import Student
from apps.courses.models import Course


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlangan'),
        ('cancelled', 'Bekor qilingan'),
        ('refunded', 'Qaytarilgan'),
    ]

    METHOD_CHOICES = [
        ('cash', 'Naqd pul'),
        ('card', 'Karta'),
        ('transfer', "Bank o'tkazma"),
        ('online', 'Online to\'lov'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments', verbose_name="Talaba")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments', verbose_name="Kurs")
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Miqdor (so'm)")
    payment_date = models.DateField(verbose_name="To'lov sanasi")
    month = models.PositiveIntegerField(verbose_name="To'lov oyi (1-12)")
    year = models.PositiveIntegerField(verbose_name="To'lov yili")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='cash', verbose_name="To'lov usuli")
    receipt_number = models.CharField(max_length=50, unique=True, verbose_name="Kvitansiya raqami")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    confirmed_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='confirmed_payments', verbose_name="Tasdiqlagan"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.amount} so'm ({self.month}/{self.year})"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            import uuid
            self.receipt_number = f"REC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class DebtRecord(models.Model):
    """Qarzdorlik yozuvi - avtomatik yoki qo'lda yaratiladi"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='debts', verbose_name="Talaba")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    month = models.PositiveIntegerField(verbose_name="Oy")
    year = models.PositiveIntegerField(verbose_name="Yil")
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Qarzdorlik miqdori")
    is_paid = models.BooleanField(default=False, verbose_name="To'langan")
    notified = models.BooleanField(default=False, verbose_name="Xabar yuborilgan")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Qarzdorlik"
        verbose_name_plural = "Qarzdorliklar"
        unique_together = ['student', 'course', 'month', 'year']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.amount} so'm ({self.month}/{self.year})"