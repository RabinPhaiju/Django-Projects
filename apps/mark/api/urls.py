from core.router import api_router

from .mark_api import MarkAPI
app_name = "mark"

api_router.register("v1/marks", MarkAPI, basename="v1_marks_api")
urlpatterns = api_router.urls
