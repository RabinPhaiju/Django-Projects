from django.urls import path
from . import views

urlpatterns = [
    path('',views.HelloOrder.as_view(),name='hello_order')
]
