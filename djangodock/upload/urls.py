from django.urls import path
from . import views

app_name = "upload" 

urlpatterns = [
    # File upload
    path("file/", views.upload_file, name="upload_file"),

    # Image upload
    path("image/", views.upload_image, name="upload_image"),
]
