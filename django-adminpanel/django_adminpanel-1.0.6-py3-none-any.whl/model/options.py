from django.db import models
from django.utils import timezone
class Options(models.Model):
	option_key = models.TextField(default="")
	option_value = models.TextField(default="")
	page_created= models.DateTimeField('created',default=timezone.now)
	page_updated= models.DateTimeField('created',default=timezone.now)