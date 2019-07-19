import pytest
from django.contrib.admin.sites import AdminSite
from mixer.backend.django import mixer
from hello import admin
from hello import models
pytestmark = pytest.mark.django_db

class TestProjectAdmin:
	def test_expect(self):
		site
