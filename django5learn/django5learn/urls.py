from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

"""
Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.
"""

urlpatterns = [
    # path("", main_views.homepage),
    path('admin/', admin.site.urls),
    # path("accounts/", include("accounts.urls")),
    path('accounts/', include('django.contrib.auth.urls')),

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