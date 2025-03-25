from django.db import models

from core.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(BaseModel):
    class StatusChoice(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
        COMPLETED = "COMPLETED", "COMPLETED"
        
    title = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=32, choices=StatusChoice.choices, default=StatusChoice.PENDING)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    