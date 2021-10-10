from django.db import models
from django.core.validators import MinLengthValidator

class Student(models.Model):
    name = models.CharField(max_length=200,
            validators=[MinLengthValidator(2, "Nickname must be greater than 1 character")]
    )
    age = models.PositiveIntegerField()
    description = models.TextField()
    date_enrolled = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
