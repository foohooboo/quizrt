from __future__ import unicode_literals

from django.db import models

class QuizResult(models.Model):
    # Contains Responses which reference the QuizResult
    date = models.DateField(required=False, null=True)

    def __str__(self):
        return "QuizResult"