from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import QuizAttempt, Topic, Question

@login_required
def home_view(request):
    return render(request, 'home.html')

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
            return redirect('/')  # Replace 'home' with your desired redirect URL
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
    if request.method == 'POST':
        topic = get_object_or_404(Topic, id=topic_id) if topic_id else None
        num_questions = int(request.POST.get('num_questions', 25))

        attempt = QuizAttempt.create_attempt(user=request.user, topic=topic, num_questions=num_questions)
        return redirect('quiz_detail', attempt_id=attempt.id)

    topics = Topic.objects.all()
    return render(request, 'start_quiz.html', {'topics': topics})

@login_required
def quiz_detail(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    questions = Question.objects.filter(id__in=attempt.quiz)

    if request.method == 'POST':
        correct_answers = []
        incorrect_answers = []

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_answer:
                correct_answers.append(question.id)
            else:
                incorrect_answers.append(question.id)

        attempt.correct_answers = correct_answers
        attempt.incorrect_answers = incorrect_answers
        attempt.finished_at = timezone.now()
        attempt.save()

        return redirect('quiz_results', attempt_id=attempt.id)

    return render(request, 'quiz_detail.html', {'attempt': attempt, 'questions': questions})

@login_required
def quiz_results(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    return render(request, 'quiz_results.html', {'attempt': attempt})