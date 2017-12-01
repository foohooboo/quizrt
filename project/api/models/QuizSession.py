from __future__ import unicode_literals

from django.utils import timezone

from django.db import models

from . import Quiz, User

class QuizSession(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False)
    session_date = models.DateTimeField(default=timezone.now)
    current_question = models.CharField(max_length=255, default='')
    display_results = models.BooleanField(default=False)

    def __str__(self):
        return "QuizSession for " + self.quiz.__str__()
    