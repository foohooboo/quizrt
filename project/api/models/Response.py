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
    
    def save(self, *args, **kwargs):
        try:
            if(self.quiz_session.is_locked):
                raise Exception('Cannot add response to closed Session')
            if(self.response_delay <= 0):
                raise Exception('Response delay cannot be zero or less')
            else:
                super(Response, self).save(*args, **kwargs)
        except AttributeError:
            raise Exception('Session required')
            
    def get_score(self):
        if self.answer.is_correct:
            return self.answer.question.question_duration // self.response_delay
        else:
            return 0
            
