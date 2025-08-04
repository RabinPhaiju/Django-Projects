from core.router import api_router

from .student_api import StudentAPI
app_name = "student"


api_router.register("v1/students", StudentAPI, basename="v1_students_api")
urlpatterns = api_router.urls
