from core.router import api_router

from .subject_api import SubjectAPI
app_name = "subject"


api_router.register("v1/subjects", SubjectAPI, basename="v1_subjects_api")
urlpatterns = api_router.urls
