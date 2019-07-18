from django.db import models
from django.utils import timezone
class Emails(models.Model):
	from_email = models.CharField(max_length=250)
	from_name = models.CharField(max_length=250)
	subject =  models.CharField(max_length=250)
	message = models.TextField(default="")
	success_message = models.TextField(default="")
	error_message = models.TextField(default="")
	email_key = models.TextField(default="")
	page_created= models.DateTimeField('created',default=timezone.now)
	page_updated= models.DateTimeField('created',default=timezone.now)
