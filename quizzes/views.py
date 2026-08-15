from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required
from courses.models import Course
from .models import Quiz, Question, Choice, StudentAnswer, QuizSubmission
from .forms import QuizForm


@teacher_required
def create_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not course.is_teacher(request.user):
        return redirect('course_list')

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.created_by = request.user
            quiz.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuizForm()

    return render(request, 'quiz_create.html', {'course': course, 'form': form})


@teacher_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.created_by != request.user:
        return redirect('course_list')

    error = None
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '').strip()
        choice_texts = request.POST.getlist('choice_text')
        correct_index = request.POST.get('correct_choice')
        valid_choices = [c for c in choice_texts if c.strip()]

        if not question_text:
            error = "Question text cannot be empty."
        elif len(valid_choices) < 2:
            error = "Please enter at least 2 choices."
        elif correct_index is None:
            error = "Please select the correct answer."
        else:
            question = Question.objects.create(quiz=quiz, text=question_text)
            for i, choice_text in enumerate(choice_texts):
                if choice_text.strip():
                    Choice.objects.create(
                        question=question, text=choice_text,
                        is_correct=(str(i) == correct_index)
                    )
            return redirect('add_question', quiz_id=quiz.id)

    return render(request, 'add_question.html', {'quiz': quiz, 'error': error})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if not quiz.course.is_enrolled(request.user):
        return redirect('course_detail', id=quiz.course.id)

    if request.method == 'POST':
        total_questions = quiz.questions.count()
        correct_count = 0

        for question in quiz.questions.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                selected_choice = get_object_or_404(Choice, id=choice_id, question=question)
                StudentAnswer.objects.update_or_create(
                    student=request.user, question=question,
                    defaults={'selected_choice': selected_choice}
                )
                if selected_choice.is_correct:
                    correct_count += 1

        score = (correct_count / total_questions * 100) if total_questions > 0 else 0
        submission = QuizSubmission.objects.create(student=request.user, quiz=quiz, score=score)
        return redirect('quiz_result', submission_id=submission.id)

    return render(request, 'quiz_take.html', {'quiz': quiz})


@login_required
def quiz_result(request, submission_id):
    submission = get_object_or_404(QuizSubmission, id=submission_id)
    if submission.student != request.user:
        return redirect('course_list')
    return render(request, 'quiz_result.html', {'submission': submission})
