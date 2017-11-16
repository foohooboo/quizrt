from __future__ import unicode_literals

from django.db import models

class ClassProfile(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    # Not sure if we need this, and the docs say it adds a performance cost
    # It might have been useful when description was required to be unique
    # class Meta:
    #    ordering = ('description',)
