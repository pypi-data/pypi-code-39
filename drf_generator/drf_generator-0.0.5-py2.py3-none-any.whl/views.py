#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .settings import VIEWSET
from .serializers import serializer_factory
# Default view setting


def view_set_factory(model, serializer=None):
    class ViewSet(VIEWSET):
        pass

    ViewSet.queryset = model.objects.all()
    ViewSet.serializer_class = serializer or serializer_factory(model)

    return ViewSet
