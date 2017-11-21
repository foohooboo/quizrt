from __future__ import unicode_literals

from django.db import models

from . import ClassProfile

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    class_profile = models.ForeignKey(ClassProfile, on_delete=models.CASCADE)


    def __str__(self):
        return self.description
