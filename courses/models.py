from django.db import models
from django.conf import settings


class Course(models.Model):
    CATEGORY_CHOICES = (
    ('fan', 'Subjects'),
    ('kasb', 'Careers'),
)

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='fan')
    cover_image = models.ImageField(upload_to='courses/', blank=True, null=True)
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CourseTeacher', related_name='courses')
    created_at = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def is_teacher(self, user):
        if not user.is_authenticated:
            return False
        return CourseTeacher.objects.filter(course=self, teacher=user).exists()

    def is_enrolled(self, user):
        if not user.is_authenticated:
            return False
        return Enrollment.objects.filter(course=self, student=user).exists()


class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'teacher')

    def __str__(self):
        return f"{self.teacher.username} — {self.course.title}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_file = models.FileField(upload_to='lessons/', blank=True, null=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


class LessonProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.username} — {self.lesson.title}"
