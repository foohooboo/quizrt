from __future__ import unicode_literals

from django.utils import timezone

from django.db import models

from . import Quiz, User

class QuizSession(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False)
    session_date = models.DateTimeField(default=timezone.now)
    current_question = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    display_results = models.BooleanField(default=False)

    # @property
    # def user_scores(self):
    #     responses_by_user = {}
    #     for response in self.response_set.all():
    #         if responses_by_user.get(response.user) != None:
    #             responses_by_user[response.user].append
    #         else:

    
    def __str__(self):
        return "QuizSession for " + self.quiz.__str__()
    