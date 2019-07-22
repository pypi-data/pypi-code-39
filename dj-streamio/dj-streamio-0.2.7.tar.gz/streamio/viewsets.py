from rest_framework.decorators import action
from rest_framework.response import Response
from .helpers import stream_view, streamactivity_view

class StreamViewSetMixin:
    """
    A mixin for using with DRF viewsets.
    Provides a GET /:resource/:id/stream/ endpoint

    """

    @action(detail=True, methods=['GET'])
    def stream(self, request, pk=None):
        return stream_view(self, request, pk=None)

    @action(detail=True, methods=['GET'])
    def streamactivity(self, request, pk=None):
        return streamactivity_view(self, request, pk=None)