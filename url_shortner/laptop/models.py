from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=200)

class Laptop(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey('Brand',on_delete=models.CASCADE,null=False)
    weight = models.FloatField()