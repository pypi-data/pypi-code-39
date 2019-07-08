from django.contrib import admin
from .models import (
	Credential,
	CallReport,
	ChatReport,
	OfflineReport,
)

class CredentialAdmin(admin.ModelAdmin):
	list_display = ('login', 'platform_id', 'user_id', 'id')
	list_filter = ('platform_id', )

	class Meta:
		model = Credential

admin.site.register(Credential, CredentialAdmin)


class CallReportAdmin(admin.ModelAdmin):
	list_display =("integration_id", "account_login", "call_id", "virtual_phone_number")
	list_filter = ('integration_id','account_login', "is_lost", 'date',)

	class Meta:
		model = CallReport

admin.site.register(CallReport, CallReportAdmin)


class ChatReportAdmin(admin.ModelAdmin):
	list_display = ('call_id', 'account_login', 'user_name', 'integration_id', 'id')
	list_filter = ('integration_id', 'date')

	class Meta:
		model = ChatReport

admin.site.register(ChatReport, ChatReportAdmin)


class OfflineReportAdmin(admin.ModelAdmin):
	list_display = ('call_id', 'account_login', 'user_name', 'integration_id', 'id')
	list_filter = ('integration_id', 'date')

	class Meta:
		model = OfflineReport

admin.site.register(OfflineReport, OfflineReportAdmin)