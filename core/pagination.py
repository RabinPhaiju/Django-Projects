from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200


class DefaultPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"
    page_size = DEFAULT_PAGE_SIZE
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data):
        if self.page_query_param not in self.request.query_params:
            return Response(data)

        next_page = self.page.next_page_number() if self.page.has_next() else None

        prev_page = (
            self.page.previous_page_number() if self.page.has_previous() else None
        )

        return Response(
            {
                "next": next_page,
                "previous": prev_page,
                "count": self.page.paginator.count,
                "results": data,
            }
        )
