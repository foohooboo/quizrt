from __future__ import unicode_literals

from django.db import models

from . import Question, Answer, User, QuizResult

class Response(models.Model):
    # user will be null for anonymous users
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE)
    
    @property
    def question(self):
        return self.answer.question

    @property
    def quiz(self):
        return self.question.quiz

    def __str__(self):
        return "Response for " + self.question.__str__()
    
    
