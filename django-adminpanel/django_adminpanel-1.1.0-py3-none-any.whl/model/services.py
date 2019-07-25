from django.db import models
from django.utils import timezone
class Service(models.Model):
	services_content = models.CharField(max_length=5000)
	services_photo = models.TextField(default="")
	services_name = models.CharField(max_length=100)
	services_created = models.DateTimeField('created',default=timezone.now)