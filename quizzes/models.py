from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    title = models.CharField(max_length=200)
    time_limit = models.PositiveIntegerField(default=0, help_text="Daqiqalarda, 0 = cheklanmagan")

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_submissions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} — {self.quiz.title} — {self.score}%"


class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'question')

    def __str__(self):
        return f"{self.student.username} answered {self.question.text}"
