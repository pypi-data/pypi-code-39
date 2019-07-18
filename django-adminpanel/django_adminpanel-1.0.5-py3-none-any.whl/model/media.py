from django.db import models
from django.utils import timezone
class Media(models.Model):
	image_title = models.TextField(default="")
	image_url = models.TextField(default="")
	page_created= models.DateTimeField('created',default=timezone.now)
	page_updated= models.DateTimeField('created',default=timezone.now)