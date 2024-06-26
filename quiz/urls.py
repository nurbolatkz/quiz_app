# quiz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('start-quiz/', views.start_quiz, name='start_quiz'),
    path('start-quiz/<int:topic_id>/', views.start_quiz, name='start_quiz_topic'),
    path('quiz/<int:attempt_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz_result/<int:attempt_id>/',
         views.quiz_result, name="quiz_result"),
    path('start-incorrect-quiz/', views.start_incorrect_quiz,
         name='start_incorrect_quiz'),
    # other paths
]
