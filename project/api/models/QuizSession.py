from __future__ import unicode_literals

from django.db import models

from . import Quiz, QuizResult, User

class QuizSession(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return "QuizSession for " + self.quiz.__str__()