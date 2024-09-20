from django.contrib import admin
from django.urls import include,path

"""
Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path("polls/", include("polls.urls")),
]
