from django.db import models

class URLData(models.Model):# creating sql query
    URLID = models.CharField(max_length=1000)
    ShortURL = models.CharField(max_length=100)

    def __str__(self):
        template = '{0.URLID},{0.ShortURL}'
        return template.format(self)

# Test
class Artist(models.Model):
    name = models.CharField(max_length=200,db_index=True,help_text='Artist name')

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=200,db_index=True,help_text='Album title')
    artist = models.ForeignKey('Artist',on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=200,db_index=True,help_text='Genre of music')

    def __str__(self):
        return self.name
    
class Track(models.Model):
    title = models.CharField(max_length=200,db_index=True,help_text='Track title')
    rating = models.IntegerField(null=True)
    length = models.IntegerField(null=True)
    count = models.IntegerField(null=True)
    album = models.ForeignKey('Album',on_delete=models.CASCADE) # if album gets deleted track get deleted
    genre = models.ForeignKey('Genre',on_delete=models.SET_NULL,null=True) # if genre gets deleted set genre as null

    def __str__(self):
        return self.title


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