from django.db import models

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=200,db_index=True,help_text='Cat name')

    def __str__(self):
        return self.name

class Dog(models.Model):
    name = models.CharField(max_length=200,db_index=True,help_text='Dog name')

    def __str__(self):
        return self.name

class Horse(models.Model):
    name = models.CharField(max_length=200,db_index=True,help_text='Horse name')

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=200,db_index=True,help_text='Car name')

    def __str__(self):
        return self.name