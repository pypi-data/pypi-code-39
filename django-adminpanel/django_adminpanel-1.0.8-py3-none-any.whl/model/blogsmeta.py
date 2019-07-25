from django.db import models
from django.utils import timezone
class Blogsmeta(models.Model):
	meta_key = models.CharField(max_length=250)
	blog_id = models.IntegerField(default=0)
	meta_value = models.TextField(default="")
	page_created= models.DateTimeField('created',default=timezone.now)
	page_updated= models.DateTimeField('created',default=timezone.now)