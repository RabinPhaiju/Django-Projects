from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path
from . import views

urlpatterns = [
    path('',RedirectView.as_view(url='/shorten/')),
    path('test/',views.test,name='test'),
    path('shorten/',views.get_form,name='urlform'),
    path('shorten/cookie',views.get_cookie,name='get_cookie'),
    path('shorten/session',views.get_session,name='get_session'),
    path('<short_url>/',views.redirect_short_url,name='redirect_function')
]
