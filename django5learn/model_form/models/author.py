from django.db import models
from django.forms import CharField, ModelForm, TextInput, Textarea
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _

TITLE_CHOICES = {
    "MR": "Mr.",
    "MRS": "Mrs.",
    "MS": "Ms.",
}


class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text= "Book name",
        error_messages={
            "unique": "Book with this name already exists.",
            "max_length": "Book name is too long.",
        },
        )
    authors = models.ManyToManyField(Author)


class AuthorForm(ModelForm):
    slug = CharField(validators=[])
    class Meta:
        model = Author
        # fields = "__all__"
        # exclude = ['id']
        fields = ["name", "title", "birth_date",'slug']
        localize_fields = ("name", "title", "birth_date")
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            },
             "name": {
                "unique": _("Author with this name already exists."),
                "max_length": _("Author name is too long."),
            },
        }
        labels = {
            "name": _("Author name"),
        }
        widgets = {
            "name": Textarea(attrs={"class": "input", "placeholder": "Enter author name",'cols':50,'rows':5}),
        }
        # formfield_callbacks
    
    # custom validation
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name == "Rabin":
            raise forms.ValidationError("Rabin is not an author")
        return name


# Form inheritance
class AuthorForm1(AuthorForm):

    class Meta(AuthorForm.Meta):
        exclude = ["name"]



class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["name", "authors"]
        # override default fields
        widgets = {
            "name": TextInput(attrs={"class": "input", "placeholder": "Enter book name"}),
        }
        labels = {
            "name": _("Book name"),
        }
        help_texts = {
            "name": _("Enter book name"),
        }
        error_messages = {
            "name": {
                "unique": _("Book with this name already exists."),
                "max_length": _("Book name is too long."),
            },
        }