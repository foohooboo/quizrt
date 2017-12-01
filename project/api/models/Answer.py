from __future__ import unicode_literals

from django.db import models

from . import Question

class Answer(models.Model):
    description = models.CharField(max_length=255, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if(self.description == ''):
            self.description = 'Answer Text Here'
        super(Quiz, self).save(*args, **kwargs)  

    def __str__(self):
        return "{0}:{1}".format(self.description, self.is_correct)
