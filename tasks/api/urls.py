from core.router import api_router

from .task_api import TaskAPI

app_name = "task"

api_router.register("v1/task", TaskAPI, basename="v1_task_api")

urlpatterns = api_router.urls
