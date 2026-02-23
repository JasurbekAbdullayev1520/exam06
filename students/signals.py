# students/signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Student, StudentDocument


@receiver(post_save, sender=Student)
def student_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Student post-save
    """
    if created:
        # Send welcome email to new student
        try:
            send_welcome_email(instance)
        except Exception as e:
            print(f"Error sending welcome email: {e}")
        
        # Log student creation
        print(f"New student created: {instance.get_full_name()} ({instance.student_id})")
        
        # Create notification for admins
        try:
            notify_admin_new_student(instance)
        except Exception as e:
            print(f"Error notifying admin: {e}")
    
    else:
        # Log student update
        print(f"Student updated: {instance.get_full_name()}")
        
        # Check for status changes
        if instance.status == 'graduated':
            try:
                send_graduation_email(instance)
            except Exception as e:
                print(f"Error sending graduation email: {e}")


@receiver(pre_delete, sender=Student)
def student_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for Student pre-delete
    """
    # Delete associated files
    if instance.profile_picture:
        instance.profile_picture.delete(save=False)
    
    # Log deletion
    print(f"Student deleted: {instance.get_full_name()} ({instance.student_id})")


@receiver(post_save, sender=StudentDocument)
def document_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for StudentDocument post-save
    """
    if created:
        # Notify student about new document
        try:
            notify_student_new_document(instance)
        except Exception as e:
            print(f"Error notifying student: {e}")


@receiver(pre_delete, sender=StudentDocument)
def document_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for StudentDocument pre-delete
    """
    # Delete the actual file
    if instance.file:
        instance.file.delete(save=False)


# Helper functions
def send_welcome_email(student):
    """Send welcome email to new student"""
    subject = 'Xush kelibsiz!'
    message = f"""
    Hurmatli {student.get_full_name()},
    
    Sizni o'quv markazimizda ko'rganimizdan xursandmiz!
    
    Sizning talaba ID raqamingiz: {student.student_id}
    
    Muvaffaqiyatlar tilaymiz!
    
    Hurmat bilan,
    O'quv markazi jamoasi
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [student.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")


def send_graduation_email(student):
    """Send graduation congratulations email"""
    subject = 'Tabriklaymiz!'
    message = f"""
    Hurmatli {student.get_full_name()},
    
    Sizni kursni muvaffaqiyatli yakunlaganingiz bilan tabriklaymiz!
    
    Kelajakda yanada yuqori muvaffaqiyatlarga erishishingizga ishonamiz.
    
    Hurmat bilan,
    O'quv markazi jamoasi
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [student.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")


def notify_admin_new_student(student):
    """Notify admins about new student registration"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Get admin users
    admins = User.objects.filter(is_staff=True)
    admin_emails = [admin.email for admin in admins if admin.email]
    
    if admin_emails:
        subject = 'Yangi talaba ro\'yxatdan o\'tdi'
        message = f"""
        Yangi talaba ro'yxatdan o'tdi:
        
        Ism: {student.get_full_name()}
        ID: {student.student_id}
        Email: {student.email}
        Telefon: {student.phone_number}
        Shahar: {student.city}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                admin_emails,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Admin notification failed: {e}")


def notify_student_new_document(document):
    """Notify student about new document upload"""
    subject = 'Yangi hujjat yuklandi'
    message = f"""
    Hurmatli {document.student.get_full_name()},
    
    Sizning profilingizga yangi hujjat yuklandi:
    
    Hujjat turi: {document.get_document_type_display()}
    Sarlavha: {document.title}
    
    Hurmat bilan,
    O'quv markazi jamoasi
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [document.student.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")