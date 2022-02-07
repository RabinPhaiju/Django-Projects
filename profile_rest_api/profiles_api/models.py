from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings # from setting.py

# Override the default user model
class UserProfileManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser should have is_staff as True")
            
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser should have is_superuser as True")
            
        if extra_fields.get('is_active') is not True:
            raise ValueError("Superuser should have is_active as True")
        
        return self.create_user(email,password,**extra_fields)


class UserProfile(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    phone = models.CharField(default='0',max_length=14)
    image=models.CharField(max_length=255,default='default.jpg')
    
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserProfileManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['name']

    def get_full_name(self):
        return self.name
    
    def __str__(self):
        return f"<User {self.email}>"


# can conside as another app
class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE # if user is deleted, delete all the feed items
    )
    status_text = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """Return the model a string"""
        return self.status_text