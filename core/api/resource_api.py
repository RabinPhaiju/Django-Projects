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

    @action(
        methods=["GET", "POST"],
        detail=False,
    )
    def permissions(self, request):
        access_policy = self.access_policy()
        statements = access_policy.get_policy_statements(request, self)
        actions = ["list", "retrieve", "create", "update", "delete"] + [
            act.__name__ for act in self.get_extra_actions()
        ]

        permissions_map = {
            action: access_policy._evaluate_statements(
                statements, request, self, action
            )
            for action in actions
        }

        return Response(
            data={
                "permissions": permissions_map,
            }
        )

    @action(
        methods=["GET", "POST"],
        detail=False,
    )
    def metadata(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        return Response(data={"fields": data.get("actions", {}).get("POST", {})})

    @extend_schema(request=BulkActionSerializer)
    @action(["post"], detail=False, url_path="bulk-action")
    def bulk_action(self, request, *args, **kwargs):
        serializer = self.bulk_action_serializer(
            data=request.data,
            context={
                "user": request.user,
                "queryset": self.filter_queryset(self.queryset),
            },
        )
        serializer.is_valid(raise_exception=True)
        result = serializer.dispatch_action()

        if result is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif isinstance(result, Response):
            return result
        else:
            return Response(data=result)
