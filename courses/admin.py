from django.contrib import admin
from .models import Course, Lesson, Enrollment, CourseTeacher, LessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)


admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(CourseTeacher)
admin.site.register(LessonProgress)
