from django import forms
from .models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'time_limit']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Quiz title'}),
            'time_limit': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': '0 = unlimited'}),
        }