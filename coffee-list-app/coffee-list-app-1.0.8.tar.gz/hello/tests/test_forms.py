from django.test import SimpleTestCase
from hello.forms import ProjectForm


class TestForms(SimpleTestCase):
    def test_project_form_valid(self):
        form = ProjectForm(
            data={"title": "capuchino", "describe": "hot", "technology": "really hot"}
        )
        self.assertTrue(form.is_valid())

    def test_project_form_no_data(self):
        form = ProjectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
