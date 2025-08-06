
from django.db.models import Q

from apps.subject.serializers.subject_serializer import SubjectLoader, SubjectSerializer
from core.roles import SYSTEM_USER
from core.api.resource_api import ResourceAPI
from core.filters.resource_filter import ResourceFilter
from core.permissions import BaseAccessPolicy
from apps.subject.models import Subject

class SubjectAccessPolicy(BaseAccessPolicy):
    statements = [
        # { "principal": "*", "action": ["list","retrieve"], "effect": "allow"},
        { "principal": f"group:{SYSTEM_USER}", "action": '*', "effect": "allow"},
    ]

class SubjectFilter(ResourceFilter):
    def q_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )

    class Meta:
        model = Subject
        fields = {
            "name": ["icontains"],
            "code": ["exact"],
        }

class SubjectAPI(ResourceAPI):
    queryset = Subject.objects.all()
    access_policy = SubjectAccessPolicy
    serializer_class = SubjectSerializer
    loader_class = SubjectLoader
    filterset_class = SubjectFilter

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return super().get_permissions()

