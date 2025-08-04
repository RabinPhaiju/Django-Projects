from typing import OrderedDict

from rest_framework.metadata import SimpleMetadata


class MinimalMetadata(SimpleMetadata):
    def get_serializer_info(self, serializer):
        fields_info = super().get_serializer_info(serializer)
        allowed_field_types = ("choice",)

        return OrderedDict(
            [
                (field, info)
                for (field, info) in fields_info.items()
                if info["type"] in allowed_field_types
            ]
        )
