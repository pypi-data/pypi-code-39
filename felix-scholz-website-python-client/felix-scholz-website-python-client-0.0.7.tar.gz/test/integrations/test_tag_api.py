
from __future__ import absolute_import

from multiprocessing.pool import AsyncResult
from pprint import pprint
from unittest import main as unittest_main

from datetime import datetime

from test.integrations.test_integration import IntegrationTestCase
from website_python_client.models.tag import Tag

from website_python_client.api.tag_api import TagApi


class TagApiTest(IntegrationTestCase):

    def setUp(self) -> None:
        super().setUp()

        self.api = TagApi(self.config)
        tag = Tag('test-' + datetime.today().isoformat())

        r = self.api.create(tag, True)
        self.tag, status, header = r.get()

    def test_create(self):
        tag = Tag('test-create_' + str(datetime.today().timestamp()))
        tag.title = 'Test 3'
        tag.title_de = 'Test de 3'

        r = self.api.create(tag, True)
        tag, status, header = r.get()
        pprint(tag)

        self.assertEqual(200, status)

    def test_show(self):
        response: AsyncResult = self.api.show(self.tag.slug, True, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)

    def test_delete(self):
        response = self.api.delete(self.tag.slug, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)

    def test_update(self):
        r = self.api.show(self.tag.slug, True, True)
        tag: Tag
        tag, status, header = r.get()

        tag.slug = 'test-update-' + datetime.today().isoformat()
        tag.title = 'updated title test lol'
        tag.title_de = 'update de title __ttt__'

        r = self.api.update(tag, ['slug', 'title', 'title_de'], True)
        tag, status, header = r.get()
        pprint(tag)

        self.assertEqual(200, status)

    def test_list(self):
        response: AsyncResult = self.api.list(None, 1, 10, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)


if __name__ == '__main__':
    unittest_main()
