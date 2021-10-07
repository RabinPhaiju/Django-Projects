from django.contrib import admin
from django.urls import path,include
from django.urls.conf import include
from Shortner import views
from . import settings
import os
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls), # keep
    path('accounts/',include('django.contrib.auth.urls')),
    path('templatee/',include('templatee.urls',namespace='template')),
    path('gview/',include('gview.urls')),
    path('laptop/',include('laptop.urls')),
    path('automobile/',include('automobile.urls')),
    path('myarticles/',include('myarticles.urls')),
    path('home/',include('home.urls')),
    path('pics/',include('pics.urls')),
    path('forum/',include('forums.urls')),
    path('chat/',include('chat.urls')),
    path('',include('Shortner.urls')),
]

# Serve the static HTML
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns += [
    url(r'^site/(?P<path>.*)$', serve,
        {'document_root': os.path.join(BASE_DIR, 'site'),
         'show_indexes': True},
        name='site_path'
        ),
]

# Serve the favicon - Keep for later
urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'home/static'),
        }
    ),
]