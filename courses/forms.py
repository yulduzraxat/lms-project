from django import forms
from .models import Course, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Course title'}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'rows': 5, 'placeholder': 'Course description'}),
            'category': forms.Select(attrs={'class': 'select-field w-full'}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Lesson title'}),
            'content': forms.Textarea(attrs={'class': 'input-field', 'rows': 6, 'placeholder': 'Lesson content'}),
        }