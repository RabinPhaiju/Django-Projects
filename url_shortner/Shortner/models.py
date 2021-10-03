from django.db import models

class URLData(models.Model):# creating sql query
    URLID = models.CharField(max_length=1000)
    ShortURL = models.CharField(max_length=100)

    def __str__(self):
        template = '{0.URLID},{0.ShortURL}'
        return template.format(self)


# Model Field Types
# AutoField
# EmailField
# FileField
# PositiveSmallintegerField
# SlugField
# BigAutoField
# BigIntegerField
# BinaryField
# FilePathField
# SmallintegerField
# FloatField
# TextFleld
# ImageField
# IntegerField
# GenericlIPAddressField ForeignKey
# NullBoolean Field
# BooleanField
# TimeField
# CharField
# URLField
# DateField
# ManyTolManyField
# DateTimeField
# DecimalField
# PositivelntegerField
# OneToOneField
# DurationField