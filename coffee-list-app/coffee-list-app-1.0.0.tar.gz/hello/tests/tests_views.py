from django.test import TestCase, Client
from hello.models import Project
from django.urls import reverse
import json


class TestViews(TestCase):
    def test_create_list_GET(self):
        client = Client()
        response = client.get(reverse("create"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "project/project_create.html")
