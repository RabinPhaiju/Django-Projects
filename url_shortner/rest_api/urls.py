from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from .models import Student
from .views import StudentView

app_name = 'rest_api'

urlpatterns = [
    path('',StudentView.as_view(),name='student'),
    path('token/',obtain_auth_token,name='obtain'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]

