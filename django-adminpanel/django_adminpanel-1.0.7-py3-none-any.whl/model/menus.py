from django.db import models
from django.utils import timezone
class Menus(models.Model):
	menu_title = models.CharField(max_length=250)
	menu_slug = models.CharField(max_length=250)
	menu_content = models.TextField(default="")
	menu_created= models.DateTimeField('created',default=timezone.now)
	menu_updated= models.DateTimeField('created',default=timezone.now)