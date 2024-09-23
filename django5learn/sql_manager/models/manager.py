from django.db import models
from django.utils.translation import gettext as _

"""
A Manager is the interface through which database query operations are provided to Django models. At least one Manager exists for every model in a Django application.
"""

class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="A")


class EditorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="E")
    
class PersonQuerySet(models.QuerySet):
    def authors(self):
        return self.filter(role="A")

    def editors(self):
        return self.filter(role="E")


class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)

    def authors(self):
        return self.get_queryset().authors()

    def editors(self):
        return self.get_queryset().editors()

class Person(models.Model):
    """ Manager names
    By default, Django adds a Manager with the name objects to every Django model class. However, if you want to use objects as a field name, or if you want to use a name other than objects for the Manager, you can rename it on a per-model basis. To rename the Manager for a given class, define a class attribute of type models.Manager() on that model
    """
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    role = models.CharField(max_length=1, choices={"A": _("Author"), "E": _("Editor")}, default="E")
    
    people = PersonManager()
    # authors = AuthorManager()
    # editors = EditorManager()



""" Modifying a manager’s initial QuerySet """
class RabsBookManager(models.Manager):
    """
    You can override a Manager’s base QuerySet by overriding the Manager.get_queryset() method. get_queryset() should return a QuerySet with the properties you require.
    """
    def get_queryset(self):
        return super().get_queryset().filter(author="Rabs Rb")

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

    def __str__(self):
        return self.title + " by " + self.author

    objects = models.Manager()  # The default manager.
    rabs_objects = RabsBookManager()  # The Dahl-specific manager.