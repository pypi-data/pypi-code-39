from django.test import TestCase, Client
from hello.models import Project
from django.urls import reverse
import json
import pytest


class TestViews(TestCase):
    def test_create_list_GET(self):
        client = Client()
        response = client.get(reverse("create"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "project/project_create.html")
    def test_create_list(self):
        client = Client()
        response = client.get(reverse("project"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "project/project.html")