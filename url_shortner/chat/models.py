from django.db import models
from django.conf import settings

# Create your models here.
class Room(models.Model) :
      name = models.CharField(max_length=1000)


class Message(models.Model) :
    text = models.TextField();
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
