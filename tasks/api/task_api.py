
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from tasks.serializers import TaskSerializer,TaskLoaderSerializer
from rest_framework.viewsets import GenericViewSet

from core.filters.resource_filter import ResourceFilter
from core.pagination import DefaultPagination
from core.permissions import BaseAccessPolicy
from tasks.models import Task


class TaskAccessPolicy(BaseAccessPolicy):
    statements = [
        { "principal": "authenticated", "action": ["list","retrieve","create", "update", "partial_update", "destroy"], "effect": "allow"},
    ]
    
class TaskFilter(ResourceFilter):
    def q_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value))
    
    class Meta:
        model = Task
        fields = {
            "description": ["icontains"],
        }

class TaskAPI(AccessViewSetMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    access_policy = TaskAccessPolicy
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    def get_serializer_class(self):
        if self.action in ("update", "create"):
            return TaskLoaderSerializer
        else:
            return self.serializer_class
    
    def get_queryset(self):
        user = self.request.user
        qs = self.queryset
        qs = qs.filter(user=user)
        return qs