# import pytest
# from django.contrib.admin.sites import AdminSite
# from mixer.backend.django import mixer
# from hello import admin
# from hello import models
# pytestmark = pytest.mark.django_db


# @pytestmark
# class TestModels:
#     def test_project(self):
#         project = mixer.blend('project.Project')
#         self.assertEquals('project.Project')
import pytest

from hello.models import Project

pytestmark = pytest.mark.django_db


class TestProject:

    def test_save():
        product = Project.objects.create(
            title="name",
            describe="text ",
            technology="description"
        )
        assert product.title == name
        assert product.describe == text
        assert product.describe == description
