from core.router import api_router

from .user_api import UserAPI

app_name = "auth"

api_router.register("v1/register", UserAPI, basename="v1_register_api")

urlpatterns = api_router.urls
