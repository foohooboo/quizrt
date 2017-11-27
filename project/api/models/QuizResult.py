from __future__ import unicode_literals

from django.db import models

class QuizResult(models.Model):
    # -AA- Contains Responses which reference the QuizResult
    # -DE- For my own dislexia, this relation is reflected in the
    # Response model's quiz_result property
    date = models.DateField(blank=True, null=True)
    