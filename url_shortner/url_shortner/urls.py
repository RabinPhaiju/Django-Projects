from django.contrib import admin
from django.urls import path,include
from django.urls.conf import include
from Shortner import views
from . import settings
import os
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls), # keep
    path('accounts/',include('django.contrib.auth.urls')),
    url(r'^oauth/',include('social_django.urls',namespace='social')),  # Keep
    path('templatee/',include('templatee.urls',namespace='template')),
    path('gview/',include('gview.urls')),
    path('laptop/',include('laptop.urls')),
    path('automobile/',include('automobile.urls')),
    path('myarticles/',include('myarticles.urls')),
    path('home/',include('home.urls')),
    path('pics/',include('pics.urls')),
    path('forum/',include('forums.urls')),
    path('chat/',include('chat.urls')),
    path('fav_products/',include('fav_products.urls')),
    path('well/',include('well.urls')),
    path('rest_api/',include('rest_api.urls')),
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

# Switch to social login if it is configured - Keep for later
try:
    from . import github_settings
    social_login = 'registration/login_social.html'
    urlpatterns.insert(0,
                       path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                       )
    print('Using', social_login, 'as the login template')
except:
    print('Using registration/login.html as the login template')

# References

# https://docs.djangoproject.com/en/3.0/ref/urls/#include
