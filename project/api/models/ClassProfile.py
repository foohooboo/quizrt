from __future__ import unicode_literals

from django.db import models

class ClassProfile(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if(self.name == ''):
            self.name = 'Profile Name Here'
        if(self.description == ''):
            self.description = 'Profile Description'
        super(ClassProfile, self).save(*args, **kwargs)  

    def __str__(self):
        return self.name
