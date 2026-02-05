from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Course
from .forms import CourseForm


def course_list(request):
    courses = Course.objects.all()
    
    search = request.GET.get('search', '')
    if search:
        courses = courses.filter(
            name__icontains=search
        ) | courses.filter(
            code__icontains=search
        )
    
    kurs_davomiligi = request.GET.get('kurs_davomiligi', '')
    if kurs_davomiligi:
        courses = courses.filter(kurs_davomiligi=kurs_davomiligi)
    
    ordering = request.GET.get('ordering', 'name')
    if ordering:
        courses = courses.order_by(ordering)
    
    context = {
        'courses': courses,
        'search': search,
        'kurs_davomiligi': kurs_davomiligi,
        'ordering': ordering
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    context = {'course': course}
    return render(request, 'courses/course_detail.html', context)


def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Kurs muvaffaqiyatli qo\'shildi!')
            return redirect('courses:course_list')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'Formada xatolar bor!')
    else:
        form = CourseForm()

    return render(request, 'courses/course_form.html', {'form': form})


def course_update(request, id):
    course = get_object_or_404(Course, id=id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kurs muvaffaqiyatli yangilandi!')
            return redirect('courses:course_detail', id=course.id)
        else:
            messages.error(request, 'Formada xatolar bor!')
    else:
        form = CourseForm(instance=course)
    
    context = {'form': form, 'course': course}
    return render(request, 'courses/course_form.html', context)


def course_delete(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == 'POST':
        course.delete()
        messages.success(request, "Kurs muvaffaqiyatli o‘chirildi")
        return redirect('courses:course_list') 

    return render(
        request,
        'courses/course_confirm_delete.html', 
        {'object': course}
    )


    
