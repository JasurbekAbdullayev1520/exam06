from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm

def student_list(request):
    students = Student.objects.all()

    min_age = request.GET.get('min_age')
    search = request.GET.get('search')

    if min_age:
        students = students.filter(age__gte=min_age)

    if search:
        students = students.filter(first_name__icontains=search)

    return render(request, 'students/student_list.html', {
        'students': students
    })

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students:student_list')
    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {
        'form': form
    })

def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'students/student_detail.html', {
        'student': student
    })
    
def student_update(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students:student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student
    })

def student_delete(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, "Talaba muvaffaqiyatli o‘chirildi")
        return redirect('students:student_list')

    return render(
        request,
        'students/student_confirm_delete.html',
        {'object': student}
    )
