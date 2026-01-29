from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import EnrollmentForm
from .models import Enrollment


def enrollment_list(request):
    enrollments = Enrollment.objects.select_related('student', 'course')

    return render(request, 'enrollments/enrollment_list.html', {
        'enrollments': enrollments
    })

def enrollment_create(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Enrollment muvaffaqiyatli qo‘shildi")
            return redirect('enrollments:enrollment_list')
    else:
        form = EnrollmentForm()

    return render(request, 'enrollments/enrollment_form.html', {
        'form': form
    })

def enrollment_update(request, id):
    enrollment = get_object_or_404(Enrollment, id=id)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, "Enrollment yangilandi")
            return redirect('enrollments:enrollment_list')
    else:
        form = EnrollmentForm(instance=enrollment)

    return render(request, 'enrollments/enrollment_form.html', {
        'form': form
    })

def enrollment_delete(request, id):
    enrollment = get_object_or_404(Enrollment, id=id)

    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, "Enrollment o‘chirildi")
        return redirect('enrollments:enrollment_list')

    return render(request, 'enrollments/enrollment_confirm_delete.html', {
        'object': enrollment
    })
