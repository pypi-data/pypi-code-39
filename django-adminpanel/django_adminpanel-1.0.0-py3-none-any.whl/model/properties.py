from django.db import models
from django.utils import timezone


PROPERTY_CHOICES = (
   ('yes', 'Yes'),
   ('no', 'No')
)
class Property(models.Model):
	property_user_type = models.CharField(max_length=250,default="")
	property_for = models.CharField(max_length=250,default="")
	property_type_of_apartment = models.CharField(max_length=250,default="")
	property_type_of_house = models.CharField(max_length=250,default="")
	property_address = models.CharField(max_length=250,default=0)
	property_info = models.CharField(max_length=250,default="")
	property_super_built_area = models.CharField(max_length=250,default="")
	property_built_area = models.CharField(max_length=250,default="")
	property_carpet_area = models.CharField(max_length=250,default="")
	property_bedroom = models.CharField(max_length=250,default="")
	property_bathroom = models.CharField(max_length=250,default="")
	property_balconies = models.CharField(max_length=250,default="")
	property_furnishing = models.CharField(max_length=250,default="")
	property_total_floor = models.CharField(max_length=250,default="")
	property_on_Floor = models.CharField(max_length=250,default="")
	property_reserved_parking = models.CharField(max_length=2,choices=PROPERTY_CHOICES)
	property_availability = models.CharField(max_length=250,default="")
	property_age_of_property = models.CharField(max_length=250,default="")
	property_expected_price = models.CharField(max_length=250,default="")
	property_contact_info = models.CharField(max_length=250,default="")
	property_inclusive_price = models.BooleanField(max_length=250,default="")
	property_inclusive_tax = models.BooleanField(default=0)
	property_img = models.TextField(default="")
	property_status = models.CharField(max_length=250,default="unpublish")
	property_brochure = models.TextField(default="")
	property_visible_date= models.DateTimeField('created',default=timezone.now)
	property_hide_date= models.DateTimeField('created',default=timezone.now)
	property_created= models.DateTimeField('created',default=timezone.now)
	property_updated= models.DateTimeField('created',default=timezone.now)