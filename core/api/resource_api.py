from django.core.exceptions import FieldDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from nested_multipart_parser.drf import DrfNestedParser
from rest_access_policy import AccessViewSetMixin
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.versioning import AcceptHeaderVersioning
from rest_framework.viewsets import ModelViewSet

from core.filters.resource_filter import ResourceFilter
from core.pagination import DefaultPagination
from core.serializers.bulk_action_serializer import BulkActionSerializer


class ResourceAPIMixins(ModelViewSet):
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    pagination_class = DefaultPagination
    parser_classes = (DrfNestedParser, JSONParser)
    versioning_class = AcceptHeaderVersioning
    bulk_action_serializer = BulkActionSerializer
    loader_class = None
    serializer_class = None
    list_serializer_class = None
    filterset_class = ResourceFilter

    def perform_create(self, serializer):
        try:
            serializer.Meta.model._meta.get_field("created_by")
            auth_user = (
                self.request.user if self.request.user.is_authenticated else None
            )
            return serializer.save(
                created_by=auth_user,
            )
        except FieldDoesNotExist:
            pass

        return super().perform_create(serializer)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        try:
            serializer.Meta.model._meta.get_field("updated_by")
            return serializer.save(updated_by=self.request.user)
        except FieldDoesNotExist:
            pass

        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

    def get_serializer_context(self):
        return {
            "request": self.request,
        }

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return self.loader_class
        elif self.action == "list" and self.list_serializer_class:
            return self.list_serializer_class
        else:
            return self.serializer_class


class ResourceAPI(AccessViewSetMixin, ResourceAPIMixins):
    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, self.queryset)
