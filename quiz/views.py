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
        quiz_data.append({
            'question': question.question_text,
            'explanation': question.explanation,
            'options': options
        })

    # Calculate quiz length
    quiz_length = len(quiz_data)

    return render(request, 'quiz_detail.html', {
        'attempt': attempt,
        'quizData': quiz_data,
        'currentQuestionIndex': 0,  # Initialize current question index
        'quizLength': quiz_length  # Pass quiz length to template
    })


@login_required
def submit_quiz(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    if request.method == 'POST':
        correct_answers = []
        incorrect_answers = []

        for question_id in attempt.quiz:
            question = get_object_or_404(Question, id=question_id)
            selected_option_label = request.POST.get(f'question_{question.id}')
            if selected_option_label is None:
                continue
            try:
                selected_option = Option.objects.get(
                    question=question.id, option_label=selected_option_label)
            except:
                print(
                    f'for this question id - {question.id}, title: {question} not founded selected_option')

            if selected_option.option_text == question.correct_answer:
                correct_answers.append(question.id)
            else:
                incorrect_answers.append(question.id)

        attempt.correct_answers = correct_answers
        attempt.incorrect_answers = incorrect_answers
        attempt.finished_at = timezone.now()
        attempt.save()

        # Update user stats
        stats, created = UserStats.objects.get_or_create(user=request.user)
        stats.quizzes_taken += 1
        stats.incorrect_answers += len(incorrect_answers)
        stats.average_stats = (stats.average_stats * (stats.quizzes_taken -
                               1) + len(correct_answers)) / stats.quizzes_taken
        stats.save()

        return redirect('quiz_result', attempt_id=attempt.id)


@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    return render(request, 'quiz_results.html', {'attempt': attempt})
