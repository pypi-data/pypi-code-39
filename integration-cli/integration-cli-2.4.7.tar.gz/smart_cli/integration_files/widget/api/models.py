from django.db import models
from django.urls import reverse
from integration_utils.fields import UTF8JSONField


class Credential(models.Model):
	login = models.CharField(max_length=255, blank=True,  null=True, default=None)
	main_user = models.CharField(max_length=255, default='main_name', blank=True, null=True)
	user_id = models.IntegerField()
	platform_id = models.CharField(max_length=100)
	
	
	class Meta:
		pass

	def __str__(self):
		return f"{self.login} - user_id:{self.user_id}, client_service_id:{self.yandex_id}"

	def get_absolute_url(self):
		return reverse('credential-detal', kwargs={"pk": self.pk})



class OfflineReport(models.Model):
	integration_id = models.IntegerField()
	smart_visitor_id = models.CharField(max_length=255, blank=True, null=True, default=None)
	account_login = models.CharField(max_length=255)
	site_id = models.IntegerField(blank=True, null=True, default=None)
	call_id = models.CharField(max_length=255)
	date = models.CharField(max_length=100, blank=True, null=True, default="")
	start_time = models.CharField(max_length=100, blank=True, null=True, default="")
	tags = UTF8JSONField(default=[])
	attributes = UTF8JSONField(default=[])
	utm_source = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_medium = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_term = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_content = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_campaign = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_referrer = models.CharField(max_length=1024, blank=True, null=True, default="none")
	metrika_cid = models.CharField(max_length=1024, blank=True, null=True, default="none")
	google_cid = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_name = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_email = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_contact_phone_number = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_description = models.CharField(max_length=1024, blank=True, null=True, default="none")
	cpn_region_name = models.CharField(max_length=1024, blank=True, null=True, default="none")
	duration = models.IntegerField(default=0)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return f"{self.integration_id}: {self.call_id} - offline_message"






class ChatReport(models.Model):
	integration_id = models.IntegerField()
	smart_visitor_id = models.CharField(max_length=255, blank=True, null=True, default=None)
	account_login = models.CharField(max_length=255)
	site_id = models.IntegerField(blank=True, null=True, default=None)
	call_id = models.CharField(max_length=255)
	date = models.CharField(max_length=100, blank=True, null=True, default="")
	start_time = models.CharField(max_length=100, blank=True, null=True, default="")
	tags = UTF8JSONField(default=[])
	attributes = UTF8JSONField(default=[])
	utm_source = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_medium = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_term = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_content = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_campaign = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_referrer = models.CharField(max_length=1024, blank=True, null=True, default="none")
	metrika_cid = models.CharField(max_length=1024, blank=True, null=True, default="none")
	google_cid = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_name = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_email = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_contact_phone_number = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_description = models.CharField(max_length=1024, blank=True, null=True, default="none")
	cpn_region_name = models.CharField(max_length=1024, blank=True, null=True, default="none")
	duration = models.IntegerField(default=0)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return f"{self.integration_id}: {self.call_id} - chat"


class CallReport(models.Model):
	integration_id = models.IntegerField()
	smart_visitor_id = models.CharField(max_length=255, blank=True, null=True, default=None)
	site_id = models.IntegerField(blank=True, null=True, default=None)
	comagic_site_id = models.IntegerField(blank=True, null=True, default=None)
	type = models.CharField(max_length=255, default='incoming_lead')
	account_login = models.CharField(max_length=255)
	call_id = models.CharField(max_length=255)
	contact_phone_number = models.CharField(max_length=25, blank=True, null=True, default=None)
	virtual_phone_number = models.CharField(max_length=255, null=True, blank=True, default="")
	cpn_region_id = models.IntegerField(blank=True, null=True, default=None)
	cpn_region_name = models.CharField(max_length=255, blank=True, null=True, default=None)
	source = models.CharField(max_length=100)
	communication_type = models.CharField(max_length=100)
	total_wait_duration = models.IntegerField()
	clean_talk_duration = models.IntegerField()
	direction = models.CharField(max_length=100)
	finish_reason = models.CharField(max_length=255)
	wait_duration = models.IntegerField()
	duration = models.IntegerField(default=0)
	finish_time = models.CharField(max_length=100)
	start_time = models.CharField(max_length=100)
	date = models.CharField(max_length=100, blank=True, null=True, default="")
	is_lost = models.BooleanField(default=False)
	tags = UTF8JSONField(default=[])
	attributes = UTF8JSONField(default=[])
	utm_source = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_medium = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_term = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_content = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_campaign = models.CharField(max_length=1024, blank=True, null=True, default="none")
	utm_referrer = models.CharField(max_length=1024, blank=True, null=True, default="none")
	metrika_cid = models.CharField(max_length=1024, blank=True, null=True, default="none")
	google_cid = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_name = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_email = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_contact_phone_number = models.CharField(max_length=1024, blank=True, null=True, default="none")
	user_description = models.CharField(max_length=1024, blank=True, null=True, default="none")

	class Meta:
		ordering = ['-call_id']

	def __str__(self):
		return f"{self.integration_id}: {self.account_login} - {self.communication_type}: {self.call_id}"