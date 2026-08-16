from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from courses.models import Enrollment, CourseTeacher


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            login(request, user)
            return redirect('course_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    user = request.user

    if user.role == 'teacher':
        course_ids = CourseTeacher.objects.filter(teacher=user).values_list('course_id', flat=True)
        courses = user.courses.filter(id__in=course_ids).annotate(
            student_count=Count('enrollments', distinct=True),
            lesson_count=Count('lessons', distinct=True),
        )
        return render(request, 'profile.html', {'courses': courses, 'role': 'teacher'})

    enrollments = Enrollment.objects.filter(student=user).select_related('course')
    courses_data = []
    for enrollment in enrollments:
        course = enrollment.course
        total_lessons = course.lessons.count()
        from courses.models import LessonProgress
        completed_count = LessonProgress.objects.filter(
            student=user, lesson__course=course, is_completed=True
        ).count()
        progress_percent = round((completed_count / total_lessons * 100)) if total_lessons > 0 else 0
        courses_data.append({
            'course': course,
            'completed_count': completed_count,
            'total_lessons': total_lessons,
            'progress_percent': progress_percent,
        })

    return render(request, 'profile.html', {'courses_data': courses_data, 'role': 'student'})
