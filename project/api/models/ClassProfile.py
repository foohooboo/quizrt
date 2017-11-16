from __future__ import unicode_literals

from django.db import models

class ClassProfile(models.Model):
    description = models.CharField(max_length=255, unique=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ('description',)
