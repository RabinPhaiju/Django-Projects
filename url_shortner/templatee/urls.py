from django.urls import path
from . import views

urlpatterns = [
    path('simple/',views.simple,name='simple'),
    path('guess/',views.guess,name='guess'),
    path('special/',views.special,name='special'),
    path('loop/',views.loop,name='loop'),
    path('nested_object/',views.nested_object,name='nested_object'),

    path('game/<slug:guess>',views.GameView.as_view())
]
