from __future__ import unicode_literals

import uuid

from django.db import models

class ClassProfile(models.Model):
    description = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ('description',)
