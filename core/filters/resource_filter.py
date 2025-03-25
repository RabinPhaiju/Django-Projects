from typing import List

from django_filters import rest_framework as filters


class ResourceFilter(filters.FilterSet):
    q = filters.CharFilter(method="q_filter", label="Search")

    def q_filter(self, *args, **kwargs):
        raise NotImplementedError('"q" filter is not implemented')

    class Meta:
        fields = ()
