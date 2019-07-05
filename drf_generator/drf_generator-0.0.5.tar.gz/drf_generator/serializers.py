#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Default serializer setting, they can specify their own serializer and
# view[set] class
# A separate serializer maker which also accepts mixins
# A separate viewset maker which also accepts mixins
# Expand?
from .settings import SERIALIZER


def serializer_factory(model, mixins=()):
    mixins = list(mixins)
    mixins.append(SERIALIZER)

    class TheSerializer(mixins[0]):
        class Meta:
            fields = "__all__"

    TheSerializer.Meta.model = model

    return TheSerializer
