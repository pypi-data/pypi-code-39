from django.db import models
from django.utils import timezone
class Testimonial(models.Model):
	testimonial = models.CharField(max_length=5000)
	client_photo = models.TextField(default="")
	client_name = models.CharField(max_length=100)
	testimonial_created = models.DateTimeField('created',default=timezone.now)