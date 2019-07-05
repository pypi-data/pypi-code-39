from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .mixins import CredentialMixin


class StandardResultsPagination(LimitOffsetPagination):
    default_limit = 1000
    max_limit = 1000


class LimitOffsetPaginationListAPIView(CredentialMixin, ListAPIView):
    """
    limit=1000
    offset=1000
    for calculation:
        rewrite get_calculation method -> dict
    for dynamic fields:
        (Need DynamicFieldSerializer)
        rewrite get_fields  method -> list
    """
    limit = None
    offset = None
    pagination_class = StandardResultsPagination

    if limit and offset:
        self.pagination_class.limit = limit
        self.pagination_class.offset = offset



    def get_calculation(self) -> dict:
        return {}


    def get_fields(self) -> list:
        return []


    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset,
            many=True,
            context={"calculation": self.get_calculation(), "fields": self.get_fields()}
        )

        return Response(serializer.data)
