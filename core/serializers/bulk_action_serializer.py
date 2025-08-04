from inspect import getmembers

from import_export import resources
from rest_framework import serializers
from rest_framework.response import Response

from core.import_export import ModelResource


def create_resource_class(model_cls, export_fields):
    BaseResource = type(  # noqa: N806
        "BaseResource",
        (ModelResource,),
        {
            "Meta": type(  # noqa: N806
                "Meta",
                (ModelResource.Meta,),
                {"fields": export_fields},
            )
        },
    )

    return resources.modelresource_factory(model_cls, BaseResource)  # noqa: N806


class BulkPublishUnpublishMixin(object):
    def action_publish(self, queryset) -> None:
        queryset.update(is_published=True)

    def action_unpublish(self, queryset) -> None:
        queryset.update(is_published=False)


class BulkActionSerializer(serializers.Serializer):
    action = serializers.CharField()
    ids = serializers.ListField(child=serializers.IntegerField())
    extras = serializers.JSONField(default={})

    class Meta:
        model = None

    def get_meta(self):
        meta = getattr(self, "Meta", None) or object
        return type("Meta", (BulkActionSerializer.Meta,), dict(meta.__dict__))

    @classmethod
    def get_actions(cls):
        return [
            (name, method)
            for name, method in getmembers(cls)
            if name.startswith("action_")
        ]

    def prepare_queryset(self, queryset):
        return queryset

    def dispatch_action(self):
        queryset = self.prepare_queryset(self.context["queryset"])
        action_name = self.data["action"]
        ids = self.data["ids"]
        action = getattr(self, action_name, None)

        if not callable(action):
            raise serializers.ValidationError(
                "There is no bulk action specified for: %s" % (action_name,)
            )

        queryset = queryset.filter(id__in=ids)

        return action(queryset)

    # def action_delete(self, queryset) -> None:
    #     queryset.delete()

    def action_archive(self, queryset) -> None:
        soft_delete = (self.data["extras"] or {}).get("soft_delete", True)
        queryset.delete(is_soft=soft_delete)

    def action_unarchive(self, queryset) -> None:
        queryset.update(is_active=True)

    def action_reorder(self, queryset) -> None:
        sequence = self.data["extras"]["sequence"]
        sequence_map = dict(  # noqa: C404
            [(rec_id, sequence := sequence + 1) for rec_id in self.data["ids"]]
        )

        for rec in queryset.order_by("sequence", "id").all():
            setattr(rec, "sequence", sequence_map[rec.id])
            rec.save()

    def action_export(self, queryset) -> Response:
        MetaClass = self.get_meta()  # noqa: N806
        Model = getattr(MetaClass, "model") or queryset.model  # noqa: N806
        extras = self.data["extras"]

        Resource = create_resource_class(Model, extras.get("fields") or ("id",))  # noqa: N806

        data = Resource().export(queryset=queryset)

        response = Response(
            data=data.csv,
            content_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": "attachment; filename=export-filename.csv",
            },
        )

        return response
