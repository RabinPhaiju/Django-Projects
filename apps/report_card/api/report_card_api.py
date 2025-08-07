from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

from apps.report_card.serializers.report_card_serializer import ReportCardSerializer,ReportCardLoader,ReportCardStudentYearSerializer,AddMarksReportCardSerializer
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
    # Optimize query by selecting related student and marks to reduce database hits
    queryset = ReportCard.objects.select_related('student').prefetch_related('marks__subject').all()
    access_policy = ReportCardAccessPolicy
    serializer_class = ReportCardSerializer
    loader_class = ReportCardLoader
    filterset_class = ReportCardFilter

    def get_serializer_class(self):
        if self.action == "student_by_year":
            return ReportCardStudentYearSerializer
        elif self.action == "add_marks":
            return AddMarksReportCardSerializer
        return super().get_serializer_class()

    @extend_schema(responses=None)
    @action(['get'],detail=False,url_path="student/(?P<student_id>[^/.]+)/year/(?P<year>[^/.]+)")
    def student_by_year(self, request, student_id, year):
        serializer = self.get_serializer(data=request.data)
        response = serializer.student_by_year(student_id=student_id,year=year)

        return Response(response,status=status.HTTP_200_OK)

    @action(['put'],detail=True,url_path="add-marks")
    def add_marks(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.add_marks(instance)

        return Response(response,status=status.HTTP_200_OK)
    