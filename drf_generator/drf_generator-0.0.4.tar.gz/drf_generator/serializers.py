#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
# Default serializer setting, they can specify their own serializer and
# view[set] class
# A separate serializer maker which also accepts mixins
# A separate viewset maker which also accepts mixins
# Expand?


def serializer_factory(model, mixins=()):
    mixins = list(mixins)
    mixins.append(serializers.HyperlinkedModelSerializer)

    class TheSerializer(mixins[0]):
        class Meta:
            fields = "__all__"

    TheSerializer.Meta.model = model

    return TheSerializer
