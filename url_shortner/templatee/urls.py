from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'templatee'

urlpatterns = [
    path('simple/',views.simple,name='simple'),
    path('guess/',views.GuessView.as_view(),name='guess'),
    path('http_response/',views.http_response.as_view(),name='http_response'),
    path('url_get/',views.url_get.as_view(),name='url_get'),
    path('url_redirect/',views.url_redirect.as_view(),name='url_redirect'),
    path('special/',views.special,name='special'),
    path('loop/',views.loop,name='loop'),
    path('nested_object/',views.nested_object,name='nested_object'),

    path('game/<slug:guess>',views.GameView.as_view(),name='game'),

    path('templatee',TemplateView.as_view(template_name='templatee/templatee.html'),name='templatee')
]
