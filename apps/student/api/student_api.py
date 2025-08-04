
from django.db.models import Q
from apps.student.serializers.student_serializer import StudentLoader, StudentSerializer

from core.roles import SYSTEM_USER
from core.api.resource_api import ResourceAPI
from core.filters.resource_filter import ResourceFilter
from core.permissions import BaseAccessPolicy
from apps.student.models import Student

class StudentAccessPolicy(BaseAccessPolicy):
    statements = [
        # { "principal": "*", "action": ["list","retrieve"], "effect": "allow"},
        { "principal": f"group:{SYSTEM_USER}", "action": '*', "effect": "allow"},
    ]

class StudentFilter(ResourceFilter):
    def q_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )

    class Meta:
        model = Student
        fields = {
            "name": ["icontains"],
            "email": ["exact"],
        }

class StudentAPI(ResourceAPI):
    queryset = Student.objects.all()
    access_policy = StudentAccessPolicy
    serializer_class = StudentSerializer
    loader_class = StudentLoader
    filterset_class = StudentFilter

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return super().get_permissions()

