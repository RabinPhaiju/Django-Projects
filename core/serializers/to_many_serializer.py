from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ToManySerializerMixin(object):
    @transaction.atomic
    def create(self, validated_data):
        meta = getattr(self, "Meta", None)
        to_many_fields = getattr(meta, "to_many_fields", [])

        for many_field in to_many_fields:
            validated_data.pop(many_field, [])

        instance = super().create(validated_data)

        for many_field in to_many_fields:
            to_many_serializer = self.fields[many_field]
            to_many_serializer.save(instance, many_field)

        # raise serializers.ValidationError('Custom error on create subject')

        return instance # .refresh_from_db()

    @transaction.atomic
    def update(self, instance, validated_data):
        meta = getattr(self, "Meta", None)
        to_many_fields = getattr(meta, "to_many_fields", [])

        for many_field in to_many_fields:
            validated_data.pop(many_field, [])

            to_many_serializer = self.fields[many_field]
            to_many_serializer.save(instance, many_field)

        return super().update(instance, validated_data)


class ToManyListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        self.initial_data = data or []

        return data

    def create(self, parent, data):
        return data

    def update(self, parent, data):
        return data

    def exec_cmd(self, cmd, rec_id, val):  # noqa: C901
        Many = self.child.Meta.model  # noqa: N806
        to_many_field = self.child.context["to_many_field"]
        parent = self.child.context["parent"]

        if cmd == 0:
            # (0, 0, {values}) link to a new record that needs to be created with the given values dictionary

            if val is None:
                raise ValueError(_("Value is not supplied"))

            data = self.create(parent, val)
            data.pop("id", None)

            assert data is not None, "`create()` did not return any data."

            self.child.run_validation(data)
            to_many_field.add(self.child.create(data))
        elif cmd == 1:
            # (1, ID, { values }) update the linked record with id = ID (write values on it)

            rec = Many.objects.get(pk=rec_id)

            if val is None:
                raise ValueError(_("Value is not supplied"))

            data = self.update(parent, val)
            data.pop("id", None)

            assert data is not None, "`update()` did not return any data."

            self.child.run_validation(data)
            self.child.update(rec, data)
        elif cmd == 2:
            # (2, ID) remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)

            rec = Many.objects.get(pk=rec_id)
            rec.delete()

            if hasattr(to_many_field, "remove"):  # Many to Many
                to_many_field.remove(rec)

        elif cmd == 3:
            # (3, ID) cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)

            rec = Many.objects.get(pk=rec_id)

            if hasattr(to_many_field, "remove"):  # Many to Many
                to_many_field.remove(rec)
            else:  # One to Many
                rec.delete()

        elif cmd == 4:
            # (4, ID) link to existing record with id = ID (adds a relationship)

            rec = Many.objects.get(pk=rec_id)  # to ensure integrity
            to_many_field.add(rec)
        elif cmd == 5:
            # (5) unlink all (like using (3,ID) for all linked records)

            if hasattr(to_many_field, "clear"):  # Many to Many
                to_many_field.clear()
            else:
                to_many_field.all().delete()
        elif cmd == 6:
            # (6, 0, [IDs]) replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)

            self.exec_cmd(5, 0, None)

            ids = val if isinstance(val, (list, tuple, set)) else [val]
            for _id in ids:
                self.exec_cmd(4, _id, None)
        else:
            raise Exception("Unknown command %s" % cmd)

    def save(self, parent, parent_field_name):
        Many = self.child.Meta.model  # noqa: N806
        errors = []

        to_many_field = getattr(parent, parent_field_name)

        self.child.context["parent"] = parent
        self.child.context["parent_field_name"] = parent_field_name
        self.child.context["to_many_field"] = to_many_field

        data = self.initial_data if hasattr(self, "initial_data") else []

        for cmd, rec_id, *val in data:
            val = val[0] if val else None

            try:
                cmd = int(cmd)
                rec_id = int(rec_id)

                self.exec_cmd(cmd, rec_id, val)
            except serializers.ValidationError as e:
                errors.append(e.detail)
            except Exception as e:
                errors.append(str(e))
            else:
                errors.append("")

        if any(errors):
            raise serializers.ValidationError({parent_field_name: errors})

        child_queryset = Many.objects.filter(**to_many_field.core_filters)

        self.validate_save(child_queryset)

    def validate_save(self, child_queryset):
        parent_field_name = self.child.context["parent_field_name"]
        count = child_queryset.count()

        data = self.initial_data if hasattr(self, "initial_data") else []
        error_code = None
        error_message = None

        if not self.allow_empty and len(data) == 0:
            error_code = "empty"
            error_message = self.error_messages[error_code]

        if self.min_length and count < self.min_length:
            error_code = "min_length"
            error_message = self.error_messages[error_code].format(
                min_length=self.min_length
            )

        if self.max_length and count > self.max_length:
            error_code = "max_length"
            error_message = self.error_messages[error_code].format(
                max_length=self.max_length
            )

        if error_message:
            raise serializers.ValidationError(
                {parent_field_name: [error_message]}, code=error_code
            )
