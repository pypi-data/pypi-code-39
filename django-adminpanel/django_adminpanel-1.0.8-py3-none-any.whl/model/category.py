from django.db import models
from django.utils import timezone
class Category(models.Model):
	title = models.CharField(max_length=250)
	cat_url = models.CharField(max_length=250)
	cat_excerpt = models.CharField(max_length=250)
	cat_image = models.CharField(max_length=250,default="")
	cat_status = models.CharField(max_length=50,default="publish")
	cat_author = models.IntegerField(default=0)
	cat_parent = models.IntegerField(default=0)
	cat_order = models.IntegerField(default=0)
	cat_created= models.DateTimeField('created',default=timezone.now)
	cat_updated= models.DateTimeField('created',default=timezone.now)