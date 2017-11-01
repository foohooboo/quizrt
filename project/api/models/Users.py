from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager)
from django.utils.translation import ugettext_lazy as _

from .ClassProfile import ClassProfile
# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, username, name,
                     email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            name=name,
            email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, name,
                    email, password, **extra_fields):
        return self._create_user(username, name,
                                 email, password,
                                 **extra_fields)

    def create_superuser(self, username, name,
                         email, password, **extra_fields):
        return self._create_user(username, name,
                                 email, password, is_superuser=True,
                                 **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    username = models.CharField(_('username'), max_length=255, unique=True)
    name = models.CharField(_('name'), max_length=255, blank=True)
    class_profiles = models.ManyToManyField(ClassProfile)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']
