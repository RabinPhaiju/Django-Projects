from django.db import models
import datetime
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from django.conf import settings
from django.core.files.storage import storages
=======
>>>>>>> 202b9c5 (added file upload)
=======
from django.conf import settings
from django.core.files.storage import storages
>>>>>>> 3662f6b (added file/image upload)
from django import forms
from django.utils import timezone
from django.contrib import admin
from django.core.files.storage import FileSystemStorage
<<<<<<< HEAD
=======
from django.utils import timezone

>>>>>>> c296fdb (added django5.1 tutorial)
=======
>>>>>>> 3662f6b (added file/image upload)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

<<<<<<< HEAD
    @admin.display(
        # decorator for method was_published_recently 
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()

        # try this for testing
        # return self.pub_date >= now - datetime.timedelta(days=1)
        
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text
=======
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    # def __str__(self):
        # return self.question_text
>>>>>>> c296fdb (added django5.1 tutorial)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
<<<<<<< HEAD
    # many-to-one relationship by default

=======
>>>>>>> c296fdb (added django5.1 tutorial)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
<<<<<<< HEAD
<<<<<<< HEAD
        return self.choice_text
    

# forms.Form
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    date = forms.DateField(widget=forms.DateInput)
    cc_myself = forms.BooleanField(required=False)

    def send_email(self):
        pass

# File Upload
class UploadFileForm(forms.Form):
    title = forms.CharField(
        label="Title",max_length=50,
        required=True,
        )
    file = forms.FileField()

# Image Upload
def select_storage():
    return FileSystemStorage(location=settings.MEDIA_ROOT)
    # return storages["mystorage"]
    # if settings.DEBUG else MyRemoteStorage()
class Car(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(storage=select_storage)

    def __str__(self):
        return self.name

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
<<<<<<< HEAD
        fields = '__all__'
=======
        return self.choice_text
>>>>>>> c296fdb (added django5.1 tutorial)
=======
        return self.choice_text
    
# File Upload
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
>>>>>>> 202b9c5 (added file upload)
=======
        fields = '__all__'
>>>>>>> 3662f6b (added file/image upload)
