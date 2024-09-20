from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name

class Laptop(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey('Brand',on_delete=models.CASCADE,null=False)
    weight = models.FloatField()

    def __str__(self) -> str:
        return self.name