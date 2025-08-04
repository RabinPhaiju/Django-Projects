from django.contrib import admin
from django.urls import path, include
from tasks.api.urls import urlpatterns as api_urls
from core.api.urls import urlpatterns as core_api_urls

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework')),
       path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += api_urls
urlpatterns += core_api_urls