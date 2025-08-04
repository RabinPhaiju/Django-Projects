
from django.db.models import Q

from apps.report_card.serializers.report_card_serializer import ReportCardSerializer,ReportCardLoader
from core.roles import SYSTEM_USER
from core.api.resource_api import ResourceAPI
from core.filters.resource_filter import ResourceFilter
from core.permissions import BaseAccessPolicy
from apps.report_card.models import ReportCard

class ReportCardAccessPolicy(BaseAccessPolicy):
    statements = [
        # { "principal": "*", "action": ["list","retrieve"], "effect": "allow"},
        { "principal": f"group:{SYSTEM_USER}", "action": '*', "effect": "allow"},
    ]

class ReportCardFilter(ResourceFilter):
    def q_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )

    class Meta:
        model = ReportCard
        fields = {
            "student": ["exact"],
            "term": ["exact"],
            "year": ["exact"],
        }

class ReportCardAPI(ResourceAPI):
    queryset = ReportCard.objects.all()
    access_policy = ReportCardAccessPolicy
    serializer_class = ReportCardSerializer
    loader_class = ReportCardLoader
    filterset_class = ReportCardFilter
