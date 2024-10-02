from django.urls import path
from . import views

# app_name = "model_form"

urlpatterns = [
    path("",views.authorForm,name="model_form"),
    path("book/",views.bookForm,name="book_form"),

]