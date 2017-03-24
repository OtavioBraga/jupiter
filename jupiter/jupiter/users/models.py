from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.db import models


import docker


# Create your models here.
class User(AbstractUser):
    bio = models.TextField('User bio')
    avatar = models.ImageField()
    data = JSONField(default={}, blank=True, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

