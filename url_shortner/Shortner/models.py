from django.db import models

# Model URL
class URLData(models.Model):# creating sql query
    URLID = models.CharField(max_length=1000)
    ShortURL = models.CharField(max_length=100)

    def __str__(self):
        template = '{0.URLID},{0.ShortURL}'
        return template.format(self)

# Model Song [Artist,Album,Genre,Track]
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

# Model Library Book
class Lang(models.Model):
    name = models.CharField(max_length=200)

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    lang = models.ForeignKey('Lang',on_delete=models.SET_NULL,null=True)

class Instance(models.Model):
    book = models.ForeignKey('Book',on_delete=models.CASCADE)
    due_back = models.DateField(null=True,blank=True)

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
# GenericlIPAddressField 
# NullBoolean Field
# BooleanField
# TimeField
# CharField
# URLField
# DateField
# ForeignKey
# ManyTolManyField
# OneToOneField
# DateTimeField
# DecimalField
# PositivelntegerField
# DurationField