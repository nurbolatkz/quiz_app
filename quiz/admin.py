
from django.contrib import admin
from .models import Question, Option, Example, UserStats, QuizAttempt

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Example)
admin.site.register(UserStats)
admin.site.register(QuizAttempt)