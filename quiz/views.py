from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import QuizAttempt, Topic, Question, UserStats, Option


@login_required
def home_view(request):
    topics = Topic.objects.all()
    return render(request, 'home.html', {'topics': topics})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(form.is_valid())  # Print the result of form validation
        if form.is_valid():
            # Form is valid, proceed with authentication
            user = form.get_user()
            login(request, user)
            # Replace 'home' with your desired redirect URL
            return redirect('/')
        else:
            print(form.errors)  # Print form errors to debug
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


@login_required
def start_quiz(request, topic_id=None):
    if request.method == "POST" and topic_id is not None:
        topic = get_object_or_404(Topic, id=topic_id)

        num_questions = int(request.POST.get('num_questions', 25))
        print(num_questions)
        attempt = QuizAttempt.create_attempt(
            user=request.user, topic=topic, num_questions=num_questions)
        return redirect('quiz_detail', attempt_id=attempt.id)

    elif request.method == "GET":
        attempt = QuizAttempt.create_attempt(
            user=request.user)
        return redirect('quiz_detail', attempt_id=attempt.id)


@login_required
def quiz_detail(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    questions = Question.objects.filter(id__in=attempt.quiz)

    # Prepare quiz data in a format suitable for JavaScript (JSON)
    quiz_data = []
    for question in questions:
        options = [option.option_text for option in question.options.all()]
        examples = [{'sentence': example.sentence, 'highlight': example.highlight}
                    for example in question.examples.all()]
        quiz_data.append({
            'question': question.question_text,
            'explanation': question.explanation,
            'options': options,
            'correct_answer': question.correct_answer,
            'examples': examples
        })

    # Calculate quiz length
    quiz_length = len(quiz_data)

    return render(request, 'quiz_detail.html', {
        'attempt': attempt,
        'quizData': quiz_data,
        'quizLength': quiz_length  # Pass quiz length to template
    })


@login_required
def quiz_result(request, attempt_id):
    if request.method == 'POST':
        correct_answers = int(request.POST.get('correct_answers'))
        incorrect_answers = int(request.POST.get('incorrect_answers'))

        attempt = get_object_or_404(
            QuizAttempt, id=attempt_id, user=request.user)
        attempt.correct_answers = correct_answers
        attempt.save()

        stats, created = UserStats.objects.get_or_create(user=request.user)
        stats.quizzes_taken += 1
        stats.incorrect_answers += int(incorrect_answers)
        stats.average_stats = (
            stats.average_stats * (stats.quizzes_taken - 1) + correct_answers) / stats.quizzes_taken
        stats.save()

        return render(request, 'quiz_results.html', {
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'attempt': attempt
        })
    else:
        return render(request, 'quiz_results.html', {})
