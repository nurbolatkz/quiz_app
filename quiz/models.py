from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=10)
    explanation = models.TextField()
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_label = models.CharField(max_length=10)
    option_text = models.TextField()

    def __str__(self):
        return f"{self.option_label}: {self.option_text}"

class Example(models.Model):
    question = models.ForeignKey(Question, related_name='examples', on_delete=models.CASCADE)
    sentence = models.TextField()
    highlight = models.TextField()

    def __str__(self):
        return self.sentence

class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes_taken = models.IntegerField(default=0)
    average_stats = models.FloatField(default=0.0)
    incorrect_answers = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.user.username}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = ArrayField(models.IntegerField(), blank=True, default=list)  # randomly selected question IDs
    total_questions = models.IntegerField()
    correct_answers = ArrayField(models.IntegerField(), blank=True, default=list)
    incorrect_answers = ArrayField(models.IntegerField(), blank=True, default=list)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Attempt {self.pk} - User: {self.user.username}"

    @classmethod
    def create_attempt(cls, user, topic=None, num_questions=25):
        if topic:
            questions = Question.objects.filter(topic=topic).order_by('?')[:num_questions]
        else:
            questions = Question.objects.order_by('?')[:num_questions]

        question_ids = [question.id for question in questions]

        return cls.objects.create(
            user=user,
            quiz=question_ids,
            total_questions=len(question_ids)
        )
