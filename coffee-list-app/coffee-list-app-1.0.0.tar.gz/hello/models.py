from django.db import models

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=100)
    describe = models.CharField(max_length=30)
    technology = models.TextField()
