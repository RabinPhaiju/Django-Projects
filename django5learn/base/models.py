from django.db import models
from django.contrib.auth.models import AbstractUser

gender_choices = [
    ('male',"Male"),
    ('female',"Female"),
    ('other',"Other"),
]
class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True,null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.TextField(null=True, default="avatar.svg")
    phone = models.CharField(default='0',max_length=14)
    gender = models.CharField(choices=gender_choices, default='other',max_length=10)

    USERNAME_FIELD = 'email'  # Email is used as the primary identifier for authentication
    REQUIRED_FIELDS = ['username']
