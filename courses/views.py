from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Q
from django.utils import timezone
from accounts.decorators import teacher_required
from .models import Course, Enrollment, CourseTeacher, Lesson, LessonProgress
from .forms import CourseForm, LessonForm
from quizzes.models import QuizSubmission


def course_list(request):
    courses = Course.objects.annotate(
        lesson_count=Count('lessons', distinct=True),
        student_count=Count('enrollments', distinct=True),
    )

    query = request.GET.get('q', '').strip()
    if query:
        courses = courses.filter(Q(title__icontains=query) | Q(description__icontains=query))

    category = request.GET.get('category')
    if category in ('fan', 'kasb'):
        courses = courses.filter(category=category)

    sort = request.GET.get('sort', 'newest')
    if sort == 'popular':
        courses = courses.order_by('-student_count')
    elif sort == 'lessons':
        courses = courses.order_by('-lesson_count')
    else:
        sort = 'newest'
        courses = courses.order_by('-created_at')

    return render(request, 'course_list.html', {
        'courses': courses,
        'selected_category': category,
        'selected_sort': sort,
        'query': query,
    })


def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    completed_lesson_ids = []
    is_enrolled = False
    is_course_teacher = False

    if request.user.is_authenticated:
        completed_lesson_ids = LessonProgress.objects.filter(
            student=request.user, lesson__course=course, is_completed=True
        ).values_list('lesson_id', flat=True)
        is_enrolled = course.is_enrolled(request.user)
        is_course_teacher = course.is_teacher(request.user)

    return render(request, 'course_detail.html', {
        'course': course,
        'completed_lesson_ids': completed_lesson_ids,
        'is_enrolled': is_enrolled,
        'is_course_teacher': is_course_teacher,
    })


@login_required
def enroll_course(request, id):
    course = get_object_or_404(Course, id=id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('course_detail', id=id)


@teacher_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            CourseTeacher.objects.create(course=course, teacher=request.user)
            return redirect('course_detail', id=course.id)
    else:
        form = CourseForm()
    return render(request, 'course_create.html', {'form': form})


@teacher_required
def create_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not course.is_teacher(request.user):
        return redirect('course_list')

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', id=course.id)
    else:
        form = LessonForm()

    return render(request, 'lesson_create.html', {'course': course, 'form': form})


@login_required
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if not lesson.course.is_enrolled(request.user):
        return redirect('course_detail', id=lesson.course.id)

    progress, _ = LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)
    progress.is_completed = True
    progress.completed_at = timezone.now()
    progress.save()
    return redirect('course_detail', id=lesson.course.id)


@teacher_required
def teacher_dashboard(request):
    course_ids = CourseTeacher.objects.filter(teacher=request.user).values_list('course_id', flat=True)
    courses = Course.objects.filter(id__in=course_ids).annotate(
        student_count=Count('enrollments', distinct=True),
        lesson_count=Count('lessons', distinct=True),
    )
    return render(request, 'teacher_dashboard.html', {'courses': courses})


@teacher_required
def course_students(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not course.is_teacher(request.user):
        return redirect('teacher_dashboard')

    total_lessons = course.lessons.count()
    enrollments = Enrollment.objects.filter(course=course).select_related('student')

    students_data = []
    for enrollment in enrollments:
        student = enrollment.student
        completed_count = LessonProgress.objects.filter(
            student=student, lesson__course=course, is_completed=True
        ).count()
        progress_percent = round((completed_count / total_lessons * 100)) if total_lessons > 0 else 0
        quiz_scores = QuizSubmission.objects.filter(student=student, quiz__course=course)

        students_data.append({
            'student': student,
            'progress_percent': progress_percent,
            'completed_count': completed_count,
            'total_lessons': total_lessons,
            'quiz_scores': quiz_scores,
        })

    return render(request, 'course_students.html', {'course': course, 'students_data': students_data})


@login_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    courses_data = []
    for enrollment in enrollments:
        course = enrollment.course
        total_lessons = course.lessons.count()
        completed_count = LessonProgress.objects.filter(
            student=request.user, lesson__course=course, is_completed=True
        ).count()
        progress_percent = round((completed_count / total_lessons * 100)) if total_lessons > 0 else 0
        courses_data.append({
            'course': course,
            'completed_count': completed_count,
            'total_lessons': total_lessons,
            'progress_percent': progress_percent,
        })
    return render(request, 'student_dashboard.html', {'courses_data': courses_data})
