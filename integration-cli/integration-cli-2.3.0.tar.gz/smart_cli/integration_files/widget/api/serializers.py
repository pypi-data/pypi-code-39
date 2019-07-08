from django.urls import reverse
from rest_framework import serializers
from .models import Credential
from .models import (
    CallReport,
    OfflineReport,
    ChatReport,

)

from config_field import ConfigSerializerMethodField


class CredentialSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Credential
        fields = [
            "id",
            "platform_id",
            "main_user",
            "user_id",
            "url"
            "login",
        ]
        extra_kwargs = {
                "id": {"read_only": True},
            }

    def get_url(self, obj):
        request  = self.context.get('request')

        return request.build_absolute_uri(reverse("credential-detail", kwargs={"pk": obj.id}))


class OfflineReportSerializer(serializers.ModelSerializer):
    user_name = ConfigSerializerMethodField(get_field='user_name', allow_empty=False)
    user_email = ConfigSerializerMethodField(get_field='user_email', allow_empty=False)
    user_description = ConfigSerializerMethodField(get_field='user_decription', allow_empty=False)
    user_contact_phone_number = ConfigSerializerMethodField(get_field='user_contact_phone_number', allow_empty=False)
    smart_visitor_id = ConfigSerializerMethodField(get_field='smart_visitor_id', allow_empty=False)
    utm_source = ConfigSerializerMethodField(get_field='utm_source', allow_empty=False)
    utm_medium = ConfigSerializerMethodField(get_field='utm_medium', allow_empty=False)
    utm_content = ConfigSerializerMethodField(get_field='utm_content', allow_empty=False)
    utm_campaign = ConfigSerializerMethodField(get_field='utm_campaign', allow_empty=False)
    utm_term = ConfigSerializerMethodField(get_field='utm_term', allow_empty=False)
    google_cid = ConfigSerializerMethodField(get_field='google_cid', allow_empty=False)
    metrika_cid = ConfigSerializerMethodField(get_field='metrika_cid', allow_empty=False)

    type = serializers.CharField(default='incoming_lead')
    communication_type = serializers.CharField(default='chat')

    class Meta:
        model = OfflineReport
        fields = (
            'integration_id',
            'site_id',
            'call_id',
            'account_login',
            'smart_visitor_id',
            'type',
            'communication_type',
            'start_time',
            'utm_source',
            'utm_medium',
            'utm_campaign',
            'utm_content',
            'utm_term',
            'google_cid',
            'metrika_cid',
            'user_name',
            'user_email',
            'user_contact_phone_number',
            'cpn_region_name',
            'duration',
            'tags',
            'attributes',
        )


class ChatReportSerializer(serializers.ModelSerializer):
    user_name = ConfigSerializerMethodField(get_field='user_name', allow_empty=False)
    user_email = ConfigSerializerMethodField(get_field='user_email', allow_empty=False)
    user_description = ConfigSerializerMethodField(get_field='user_decription', allow_empty=False)
    user_contact_phone_number = ConfigSerializerMethodField(get_field='user_contact_phone_number', allow_empty=False)
    smart_visitor_id = ConfigSerializerMethodField(get_field='smart_visitor_id', allow_empty=False)
    utm_source = ConfigSerializerMethodField(get_field='utm_source', allow_empty=False)
    utm_medium = ConfigSerializerMethodField(get_field='utm_medium', allow_empty=False)
    utm_content = ConfigSerializerMethodField(get_field='utm_content', allow_empty=False)
    utm_campaign = ConfigSerializerMethodField(get_field='utm_campaign', allow_empty=False)
    utm_term = ConfigSerializerMethodField(get_field='utm_term', allow_empty=False)
    google_cid = ConfigSerializerMethodField(get_field='google_cid', allow_empty=False)
    metrika_cid = ConfigSerializerMethodField(get_field='metrika_cid', allow_empty=False)

    type = serializers.CharField(default='incoming_lead')
    communication_type = serializers.CharField(default='chat')

    class Meta:
        model = ChatReport
        fields = (
            'integration_id',
            'site_id',
            'call_id',
            'account_login',
            'smart_visitor_id',
            'type',
            'communication_type',
            'start_time',
            'utm_source',
            'utm_medium',
            'utm_campaign',
            'utm_content',
            'utm_term',
            'google_cid',
            'metrika_cid',
            'user_name',
            'user_email',
            'user_contact_phone_number',
            'cpn_region_name',
            'duration',
            'tags',
            'attributes',
        )


class CallReportSerializer(serializers.ModelSerializer):
    user_name = ConfigSerializerMethodField(get_field='user_name', allow_empty=False)
    user_email = ConfigSerializerMethodField(get_field='user_email', allow_empty=False)
    user_description = ConfigSerializerMethodField(get_field='user_decription', allow_empty=False)
    user_contact_phone_number = ConfigSerializerMethodField(get_field='user_contact_phone_number', allow_empty=False)
    smart_visitor_id = ConfigSerializerMethodField(get_field='smart_visitor_id', allow_empty=False)
    utm_source = ConfigSerializerMethodField(get_field='utm_source', allow_empty=False)
    utm_medium = ConfigSerializerMethodField(get_field='utm_medium', allow_empty=False)
    utm_content = ConfigSerializerMethodField(get_field='utm_content', allow_empty=False)
    utm_campaign = ConfigSerializerMethodField(get_field='utm_campaign', allow_empty=False)
    utm_term = ConfigSerializerMethodField(get_field='utm_term', allow_empty=False)
    google_cid = ConfigSerializerMethodField(get_field='google_cid', allow_empty=False)
    metrika_cid = ConfigSerializerMethodField(get_field='metrika_cid', allow_empty=False)

    type = serializers.CharField(default='incoming_lead')
    communication_type = serializers.CharField(default='chat')

    class Meta:
        model = CallReport
        fields = (
            'integration_id',
            'account_login',
            'smart_visitor_id',
            'type',
            'call_id',
            'user_contact_phone_number',
            'virtual_phone_number',
            'cpn_region_id',
            'cpn_region_name',
            'source',
            'site_id',
            'comagic_site_id',
            'communication_type',
            'total_wait_duration',
            'clean_talk_duration',
            'direction',
            'finish_reason',
            'wait_duration',
            'start_time',
            # 'finish_time',
            'duration',
            # 'date',
            'tags',
            'attributes',
            'utm_source',
            'utm_medium',
            'utm_term',
            'utm_content',
            'utm_campaign',
            'utm_referrer',
            'user_name',
            'user_email',
            'user_description',
            'metrika_cid',
            'google_cid',
        )

    def get_user_name(self, obj):
        return 'none'

    def get_user_email(self, obj):
        return 'none'

    def get_user_description(self, obj):
        return 'none'

    def get_user_contact_phone_number(self, obj):
        return obj.contact_phone_number

