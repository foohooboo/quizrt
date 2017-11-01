from __future__ import unicode_literals

import uuid

from django.db import models

from . import ClassProfile

class Quiz(models.Model):
    description = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    class_profile = models.ForeignKey(ClassProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
