# students/apps.py
from django.apps import AppConfig


class StudentsConfig(AppConfig):
    """
    Students app configuration
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'
    verbose_name = 'Talabalar Boshqaruvi'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import students.signals
        except ImportError:
            pass