from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls

"""
Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.
"""

urlpatterns = [
    # path("", main_views.homepage),
    path('admin/', admin.site.urls),
    path("polls/", include("polls.urls")),
    path("topic_http/", include("topic_http.urls")),
]


# for debug toolbar
if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()