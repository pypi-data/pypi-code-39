from django.test import SimpleTestCase
from django.urls import reverse, resolve
from hello.views import project_create_view, project_views


class TestUrls(SimpleTestCase):
    def test_create_url_is_resolved(self):
        url = reverse("create")
        self.assertEqual(resolve(url).func, project_create_view)

    def test_project_url_is_resolved(self):
        url = reverse("project")
        self.assertEqual(resolve(url).func, project_views)
