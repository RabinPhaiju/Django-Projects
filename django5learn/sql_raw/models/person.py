from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    birth_date = models.DateField(null=True)