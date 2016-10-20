# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from rest_framework.authtoken.models import Token


@python_2_unicode_compatible
class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='avatars/', default='avatars/default_avatar.jpg')

    @property
    def token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
