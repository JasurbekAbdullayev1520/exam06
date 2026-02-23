"""
====================================================
Payments Views — To'lovlar moduli
====================================================
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.http import HttpResponse
import csv
import datetime

from .models import Payment, DebtRecord
from apps.students.models import Student
from apps.courses.models import Course


@login_required
def payment_list(request):
    """To'lovlar ro'yxati + filtrlash"""
    payments = Payment.objects.select_related('student', 'course', 'confirmed_by').all()

    # — Filtrlar —
    student_id = request.GET.get('student')
    course_id = request.GET.get('course')
    status = request.GET.get('status')
    month = request.GET.get('month')
    year = request.GET.get('year')
    method = request.GET.get('method')

    if student_id:
        payments = payments.filter(student_id=student_id)
    if course_id:
        payments = payments.filter(course_id=course_id)
    if status:
        payments = payments.filter(status=status)
    if month:
        payments = payments.filter(month=month)
    if year:
        payments = payments.filter(year=year)
    if method:
        payments = payments.filter(method=method)

    # — Statistika —
    total_confirmed = payments.filter(status='confirmed').aggregate(Sum('amount'))['amount__sum'] or 0
    total_pending = payments.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0

    # — CSV Export —
    if request.GET.get('export') == 'csv':
        return export_payments_csv(payments)

    context = {
        'payments': payments,
        'all_students': Student.objects.all().order_by('first_name'),
        'all_courses': Course.objects.filter(is_active=True),
        'total_confirmed': total_confirmed,
        'total_pending': total_pending,
        'current_year': timezone.now().year,
        'months': list(range(1, 13)),
    }
    return render(request, 'payments/payment_list.html', context)


@login_required
def payment_create(request):
    """Yangi to'lov qo'shish"""
    if request.method == 'POST':
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        month = request.POST.get('month')
        year = request.POST.get('year')
        method = request.POST.get('method', 'cash')
        notes = request.POST.get('notes', '')

        try:
            payment = Payment.objects.create(
                student_id=student_id,
                course_id=course_id,
                amount=amount,
                payment_date=payment_date,
                month=month,
                year=year,
                method=method,
                notes=notes,
                status='confirmed',
                confirmed_by=request.user,
            )
            # Qarzdorlikni yangilash
            DebtRecord.objects.filter(
                student_id=student_id,
                course_id=course_id,
                month=month,
                year=year
            ).update(is_paid=True)

            messages.success(request, f"To'lov muvaffaqiyatli qabul qilindi. Kvitansiya: {payment.receipt_number}")
            return redirect('payments:payment_list')

        except Exception as e:
            messages.error(request, f"Xatolik: {str(e)}")

    context = {
        'students': Student.objects.filter(status='active').order_by('first_name'),
        'courses': Course.objects.filter(is_active=True),
        'current_month': timezone.now().month,
        'current_year': timezone.now().year,
        'months': list(range(1, 13)),
        'years': list(range(2020, timezone.now().year + 2)),
    }
    return render(request, 'payments/payment_form.html', context)


@login_required
def debt_list(request):
    """Qarzdorlar ro'yxati"""
    debts = DebtRecord.objects.select_related('student', 'course').filter(is_paid=False)

    search = request.GET.get('search', '')
    course_id = request.GET.get('course')

    if search:
        debts = debts.filter(
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(student__phone_number__icontains=search)
        )
    if course_id:
        debts = debts.filter(course_id=course_id)

    total_debt = debts.aggregate(Sum('amount'))['amount__sum'] or 0

    if request.GET.get('export') == 'csv':
        return export_debts_csv(debts)

    context = {
        'debts': debts,
        'all_courses': Course.objects.filter(is_active=True),
        'total_debt': total_debt,
        'debtors_count': debts.values('student').distinct().count(),
    }
    return render(request, 'payments/debt_list.html', context)


@login_required
def student_payment_history(request, student_id):
    """Bitta talabaning to'lov tarixi"""
    student = get_object_or_404(Student, id=student_id)
    payments = Payment.objects.filter(student=student).select_related('course').order_by('-payment_date')
    debts = DebtRecord.objects.filter(student=student, is_paid=False).select_related('course')

    total_paid = payments.filter(status='confirmed').aggregate(Sum('amount'))['amount__sum'] or 0
    total_debt = debts.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'student': student,
        'payments': payments,
        'debts': debts,
        'total_paid': total_paid,
        'total_debt': total_debt,
    }
    return render(request, 'payments/student_payment_history.html', context)


def export_payments_csv(payments):
    """To'lovlarni CSV formatida yuklab olish"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="tolovlar_{datetime.date.today()}.csv"'
    response.write('\ufeff')  # UTF-8 BOM for Excel

    writer = csv.writer(response)
    writer.writerow(['Kvitansiya', 'Talaba', 'Kurs', 'Miqdor', 'Oy', 'Yil', 'Holat', 'Usul', 'Sana'])

    for p in payments:
        writer.writerow([
            p.receipt_number,
            p.student.get_full_name(),
            p.course.name,
            p.amount,
            p.month,
            p.year,
            p.get_status_display(),
            p.get_method_display(),
            p.payment_date,
        ])
    return response


def export_debts_csv(debts):
    """Qarzdorlikni CSV formatida yuklab olish"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="qarzdorlar_{datetime.date.today()}.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(['Talaba', 'Telefon', 'Kurs', 'Miqdor', 'Oy', 'Yil'])

    for d in debts:
        writer.writerow([
            d.student.get_full_name(),
            d.student.phone_number,
            d.course.name,
            d.amount,
            d.month,
            d.year,
        ])
    return response
