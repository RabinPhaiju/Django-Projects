from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

app_name = "report_card_system"
api_urls = [
    path("", include("core.api.urls")),
    path("", include("apps.student.api.urls")),
    path("", include("apps.subject.api.urls")),
    path("", include("apps.report_card.api.urls")),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path("api/", include(api_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)