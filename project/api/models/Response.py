from __future__ import unicode_literals

from django.db import models

from . import Question, Answer, User

class Response(models.Model):
    # user will be null for anonymous users
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return "Response for " + self.question.__str__()
    
    @property
    def quiz(self):
        return self.question.quiz
    