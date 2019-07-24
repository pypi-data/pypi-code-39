from django.db import models
from django.utils import timezone
class Usermeta(models.Model):
	meta_key = models.TextField(default="")
	meta_value = models.TextField(default="")
	user_id = models.IntegerField(default=0)
	page_created= models.DateTimeField('created',default=timezone.now)
	page_updated= models.DateTimeField('created',default=timezone.now)