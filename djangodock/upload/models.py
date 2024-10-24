from django.db import models
from django.conf import settings
from django import forms
from django.core.files.storage import FileSystemStorage

# File Upload
class UploadFileForm(forms.Form):
    title = forms.CharField(label="Title",max_length=50,required=True)
    file = forms.FileField()

# Image Upload
def select_storage():
    return FileSystemStorage(location=settings.MEDIA_ROOT)
    # return storages["mystorage"]
    # if settings.DEBUG else MyRemoteStorage()

class ProfileImage(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(storage=select_storage)

    def __str__(self):
        return self.name

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = '__all__'