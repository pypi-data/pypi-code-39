from django.db import models
from django.utils import timezone
class Package(models.Model):
	package_name = models.CharField(max_length=250)
	package_price = models.TextField(default="")
	package_type = models.TextField(default="")
	package_details = models.TextField(default="")
	package_status = models.CharField(max_length=250,default="")
	package_for = models.CharField(max_length=250,default="")
	package_time = models.CharField(max_length=250,default="")
	package_vat = models.CharField(max_length=250,default="")
	package_vatamt = models.CharField(max_length=250,default="")
	stipe_product_id = models.CharField(max_length=250,default="")
	stipe_plan_id = models.CharField(max_length=250,default="")
	package_created= models.DateTimeField('created',default=timezone.now)
	package_updated= models.DateTimeField('created',default=timezone.now)