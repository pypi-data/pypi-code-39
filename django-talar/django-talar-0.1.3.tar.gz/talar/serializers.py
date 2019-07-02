from rest_framework import serializers


class TalarSerializer(serializers.Serializer):
    external_id = serializers.CharField(max_length=255)
    amount = serializers.CharField(max_length=255)
    currency = serializers.CharField(max_length=255)
    continue_url = serializers.CharField(max_length=255)
    provider_code = serializers.CharField(max_length=255, required=False,
                                          allow_blank=True)
