from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django_lifecycle import LifecycleModelMixin

from core.models import BaseModelManager



class UserManager(BaseModelManager, BaseUserManager):
    pass


class GroupManager(BaseModelManager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def get_queryset(self):
        return models.QuerySet(self.model, using=self._db)


Group.objects = GroupManager()
Group.objects.model = Group


class User(LifecycleModelMixin, AbstractUser):
    email = models.EmailField(unique=True)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = UserManager()

    def __str__(self):
        return self.email