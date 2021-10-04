from django.urls import path
from . import views

app_name = 'laptop'

urlpatterns = [
    path('laptop/',views.LaptopView.as_view(),name='laptop'),

]
