from __future__ import unicode_literals

import uuid

from django.db import models

from . import Question

class Answer(models.Model):
    description = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return "{0}:{1}".format(self.description, self.is_correct)
