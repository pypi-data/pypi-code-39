from django.test import TestCase, RequestFactory
from projects.models import Project
from django.urls import reverse
from .views import project_detail as pd
from .apps import ProjectsConfig
from django.apps import apps

# Create your tests here.


class ProjectModelTest(TestCase):
    """docstring for ProjectModelTest"""

    def create_project(self, ptitle="only a test", pdes="yes, this is only a test", ptech="yes, this is only a test", pimg="yes, this is only a test"):
        return Project.objects.create(title=ptitle, description=pdes, technology=ptech, image=pimg)

    def test_projects_title(self):
        tit = self.create_project()
        self.assertTrue(isinstance(tit, Project))
        self.assertEqual(tit.project_title(), tit.title)

    def test_projects_description(self):
        pdesc = self.create_project()
        self.assertTrue(isinstance(pdesc, Project))
        self.assertEqual(pdesc.project_description(), pdesc.description)

    def test_projects_technology(self):
        ptechn = self.create_project()
        self.assertTrue(isinstance(ptechn, Project))
        self.assertEqual(ptechn.project_technology(), ptechn.technology)

    def test_projects_image(self):
        pimge = self.create_project()
        self.assertTrue(isinstance(pimge, Project))
        self.assertEqual(pimge.project_image(), pimge.image)

    def test_project_index_view_uses_correct_template(self):
        response = self.client.get(reverse('project_index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'project_index.html')

    def test_project_detail_view_uses_correct_template(self):
        self.factory = RequestFactory()
        self.dv = self.create_project()

        request = self.factory.get("<int:pk>")
        request.dv = self.dv
        response = pd(request, 1)
        self.assertEqual(response.status_code, 200)


class TestProjectApps(TestCase):
    """docstring for TestApps"""

    def test_project_apps(self):
        self.assertEqual(ProjectsConfig.name, "projects")
        self.assertEqual(apps.get_app_config("projects").name, "projects")
