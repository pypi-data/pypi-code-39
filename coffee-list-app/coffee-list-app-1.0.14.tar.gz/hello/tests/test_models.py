from django.test import TestCase

from hello.models import Project
import pytest


class TestProject(TestCase):

    def setUp(self):
        self.project1 = Project.objects.create(

            title="name",
            describe="text ",
            technology="description"
        )
