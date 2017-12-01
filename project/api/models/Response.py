from __future__ import unicode_literals

from django.db import models

from . import Question, Answer, User, QuizSession

class Response(models.Model):
    # user will be null for anonymous users
    user = models.CharField(max_length=255)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    response_delay = models.IntegerField(default=0)
    
    @property
    def question(self):
        return self.answer.question

    @property
    def quiz(self):
        return self.question.quiz

    def __str__(self):
        return "Response for " + self.question.__str__()
    
    def get_score(self):
        if self.answer.is_correct:
            return self.answer.question.question_duration / self.response_delay
        else:
            return 0
            