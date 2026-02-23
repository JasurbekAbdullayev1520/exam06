"""
====================================================
Attendance Views — Davomat moduli
====================================================
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q

from .models import Lesson, Attendance
from apps.courses.models import Group
from apps.students.models import Student
from apps.enrollments.models import Enrollment


@login_required
def lesson_list(request):
    """Darslar ro'yxati"""
    if request.user.is_teacher and not request.user.is_manager:
        lessons = Lesson.objects.filter(group__instructor=request.user)
    else:
        lessons = Lesson.objects.all()

    lessons = lessons.select_related('group', 'group__course', 'created_by').order_by('-date')

    context = {'lessons': lessons}
    return render(request, 'attendance/lesson_list.html', context)


@login_required
def lesson_create(request):
    """Yangi dars qo'shish"""
    if request.user.is_teacher and not request.user.is_manager:
        groups = Group.objects.filter(instructor=request.user, is_active=True)
    else:
        groups = Group.objects.filter(is_active=True)

    if request.method == 'POST':
        group_id = request.POST.get('group')
        date = request.POST.get('date')
        topic = request.POST.get('topic', '')

        group = get_object_or_404(Group, id=group_id)

        lesson, created = Lesson.objects.get_or_create(
            group=group, date=date,
            defaults={'topic': topic, 'created_by': request.user}
        )

        if not created:
            messages.warning(request, "Bu sana uchun dars allaqachon mavjud.")
            return redirect('attendance:take_attendance', lesson_id=lesson.id)

        # Guruh talabalarini avtomatik qo'shish
        enrollments = Enrollment.objects.filter(group=group, status='active').select_related('student')
        attendance_records = [
            Attendance(lesson=lesson, student=e.student, status='absent')
            for e in enrollments
        ]
        Attendance.objects.bulk_create(attendance_records, ignore_conflicts=True)

        messages.success(request, "Dars yaratildi. Endi davomatni belgilang.")
        return redirect('attendance:take_attendance', lesson_id=lesson.id)

    context = {'groups': groups}
    return render(request, 'attendance/lesson_form.html', context)


@login_required
def take_attendance(request, lesson_id):
    """Davomat belgilash"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    attendances = Attendance.objects.filter(lesson=lesson).select_related('student')

    if request.method == 'POST':
        for attendance in attendances:
            status = request.POST.get(f'status_{attendance.id}', 'absent')
            notes = request.POST.get(f'notes_{attendance.id}', '')
            attendance.status = status
            attendance.notes = notes
            attendance.save()

        messages.success(request, "Davomat saqlandi!")
        return redirect('attendance:lesson_list')

    total = attendances.count()
    present = attendances.filter(status='present').count()

    context = {
        'lesson': lesson,
        'attendances': attendances,
        'total': total,
        'present': present,
        'attendance_rate': round(present / total * 100, 1) if total > 0 else 0,
    }
    return render(request, 'attendance/take_attendance.html', context)
