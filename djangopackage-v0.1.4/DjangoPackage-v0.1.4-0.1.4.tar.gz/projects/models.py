from django.db import models

from django_prometheus.models import ExportModelOperationsMixin


class Project(ExportModelOperationsMixin('project'), models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    image = models.FilePathField(path="/img")

    def project_title(self):
        return self.title

    def project_description(self):
        return self.description

    def project_technology(self):
        return self.technology

    def project_image(self):
        return self.image
