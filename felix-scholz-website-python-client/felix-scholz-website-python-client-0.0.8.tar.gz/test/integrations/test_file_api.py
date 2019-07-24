
from __future__ import absolute_import

from datetime import datetime
from multiprocessing.pool import AsyncResult
from pprint import pprint
from unittest import main as unittest_main

from test.integrations.test_integration import IntegrationTestCase
from website_python_client.models.file import File

from website_python_client.api.file_api import FileApi


class FileApiTest(IntegrationTestCase):

    def setUp(self) -> None:
        super().setUp()

        self.api = FileApi(self.config)
        file = File.create_from_path(self.generate_test_image('test+api+file+setup' + str(datetime.today().timestamp())),
                                     False, 'Test Title', 'Test Description')
        file.title = 'test api file setup ' + str(datetime.today().timestamp())

        r = self.api.create(file, True)
        self.file, status, header = r.get()

    def test_create(self):
        file = File.create_from_path(self.generate_test_image('test+api+file+create' + str(datetime.today().timestamp())),
                                     False, 'Test Title', 'Test Description')

        r = self.api.create(file, True)
        file, status, header = r.get()
        pprint(file)

        self.assertIn(status, [250, 200])

    def test_show(self):
        identifier = self.file.identifier
        response: AsyncResult = self.api.show(identifier, False, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)

    def test_delete(self):
        identifier = self.file.identifier
        response = self.api.delete(identifier, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)

    def test_update(self):
        identifier = self.file.identifier
        r = self.api.show(identifier, True, True)
        file: File
        file, status, header = r.get()

        file.title = 'updated title'
        file.public = True

        r = self.api.update(file, ['title', 'public'], True)
        file, status, header = r.get()
        pprint(file)

        self.assertEqual(200, status)

    def test_list(self):
        response: AsyncResult = self.api.list(1, 10, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)


if __name__ == '__main__':
    unittest_main()
