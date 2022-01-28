from django.urls import path
from . import views

urlpatterns = [
    path('',views.HelloAuth.as_view(),name='hello_auth')
]
