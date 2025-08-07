
from django.db.models import Q

from apps.mark.serializers.marks_serializer import MarkLoader, MarkSerializer
from core.roles import SYSTEM_USER
from core.api.resource_api import ResourceAPI
from core.filters.resource_filter import ResourceFilter
from core.permissions import BaseAccessPolicy
from apps.mark.models import Mark

class MarkAccessPolicy(BaseAccessPolicy):
    statements = [
        # { "principal": "*", "action": ["list","retrieve"], "effect": "allow"},
        { "principal": f"group:{SYSTEM_USER}", "action": '*', "effect": "allow"},
    ]

class MarkFilter(ResourceFilter):
    def q_filter(self, queryset, name, value):
        return queryset.filter(
            Q(subject__name__icontains=value)
        )

    class Meta:
        model = Mark
        fields = {
            "report_card__term": ["icontains"],
            "report_card__year": ["exact"],
        }

class MarkAPI(ResourceAPI):
    queryset = Mark.objects.select_related('subject').all()
    access_policy = MarkAccessPolicy
    serializer_class = MarkSerializer
    loader_class = MarkLoader
    filterset_class = MarkFilter
