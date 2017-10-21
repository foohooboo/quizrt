from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager)
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class BaseUserManager(BaseUserManager):

    def _create_user(self, username, first_name, last_name,
                     email, password, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_superuser=is_superuser,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, first_name, last_name,
                    email, password, **extra_fields):
        return self._create_user(username, first_name, last_name,
                                 email, password, is_superuser=False,
                                 **extra_fields)

    def create_superuser(self, username, first_name, last_name,
                         email, password, **extra_fields):
        return self._create_user(username, first_name, last_name,
                                 email, password, is_superuser=True,
                                 **extra_fields)

class BaseUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    uuid = models.SlugField(default=uuid.uuid4, editable=False)
    username = models.CharField(_('username'), max_length=255, default='temp')
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    is_superuser = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
