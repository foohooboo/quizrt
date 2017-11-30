from __future__ import unicode_literals

from django.db import models

class ClassProfile(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if (self.name == ''):
            raise TypeError('Name cannot be blank')
        if (self.description == ''):
            raise TypeError('Description cannot be blank')
        else:
            super(ClassProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
