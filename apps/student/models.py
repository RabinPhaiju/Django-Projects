from core.models import BaseModel
from django.db import models

class Student(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name