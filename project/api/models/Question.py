from __future__ import unicode_literals

from django.db import models

from . import Quiz

class Question(models.Model):
    prompt = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    order_number = models.IntegerField(default=0)
    question_duration = models.IntegerField(default=30)

    def save(self, *args, **kwargs):
        if(self.name == ''):
            self.name = 'Question Name Here'
        if(self.prompt == ''):
            self.prompt = 'Question Prompt'
        if(self.question_duration <= 0):
            self.question_duration *= -1
        super(Question, self).save(*args, **kwargs) 

    def __str__(self):
        return self.name