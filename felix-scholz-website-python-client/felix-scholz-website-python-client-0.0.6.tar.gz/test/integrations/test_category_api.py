
from __future__ import absolute_import

from multiprocessing.pool import AsyncResult
from pprint import pprint
from unittest import main as unittest_main

from datetime import datetime

from test.integrations.test_integration import IntegrationTestCase
from website_python_client.models.category import Category

from website_python_client.api.category_api import CategoryApi


class CategoryApiTest(IntegrationTestCase):

    def setUp(self) -> None:
        super().setUp()

        self.api = CategoryApi(self.config)
        category = Category(Category.hash_identifier('test_' + str(datetime.today().timestamp())))
        category.title = 'Test api category setup'
        category.slug = 'test-api-category-setup'

        response = self.api.create(category, True)
        self.category, status, header = response.get()

    def test_create(self):
        category = Category(Category.hash_identifier('test_12343181' + str(datetime.today().timestamp())))
        category.title = 'sec category'
        category.slug = 'sec-category'
        category.parent_id = self.category.parent_id
        category.source = 'test_32'
        category.description = 'test sd description'
        category.acl.group.append('testG')
        category.acl.group.append('testG_less')
        category.acl.user.append('testU')

        response = self.api.create(category, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)

    def test_show(self):
        response: AsyncResult = self.api.show(self.category.identifier, True, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)

    def test_delete(self):
        response = self.api.delete(self.category.identifier, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)

    def test_update(self):
        identifier = self.category.identifier
        r = self.api.show(identifier, True, True)
        category: Category
        category, status, header = r.get()
        self.assertEqual(200, status)

        category.title = 'updated title'
        category.slug = 'update-slug-e'
        category.acl.group.append('test_group_update')

        r = self.api.update(category, ['title', 'slug', 'acl'], True)
        category, status, header = r.get()
        pprint(category)

    def test_list(self):
        response: AsyncResult = self.api.list(1, 10, True)
        r, status, header = response.get()
        pprint(r)

        self.assertEqual(200, status)


if __name__ == '__main__':
    unittest_main()
