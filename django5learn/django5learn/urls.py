from django.contrib import admin
from django.urls import include,path
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from base import views as base_views
=======
>>>>>>> c296fdb (added django5.1 tutorial)

"""
Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.
"""

urlpatterns = [
<<<<<<< HEAD
    path("", base_views.homepage, name="homepage"),
    path('admin/', admin.site.urls),
    # path('', include('django.contrib.auth.urls')),
    path("", include("base.urls")),

    path("polls/", include("polls.urls")),
    path("topic_http/", include("topic_http.urls")),
    path("model_form/", include("model_form.urls")),
]

# add image media path
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# for debug toolbar
if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
=======
    path('admin/', admin.site.urls),
    path("polls/", include("polls.urls")),
]
>>>>>>> c296fdb (added django5.1 tutorial)
