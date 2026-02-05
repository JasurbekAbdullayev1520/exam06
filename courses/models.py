from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, verbose_name='Kurs kodi')
    description = models.TextField(blank=True, null=True)
    oylik_tolov = models.BigIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10000000),
                    ]
    )
    kurs_davomiligi = models.BigIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(12),
        ]
    )
    year = models.BigIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3000)
        ]
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'

    def __str__(self):
        return f"{self.code} - {self.name}"

