
from __future__ import absolute_import

from pprint import pprint
from unittest import main as unittest_main

from datetime import datetime

from test.integrations.test_integration import IntegrationTestCase
from website_python_client.api.post_api import PostApi

from website_python_client.models.author import Author

from website_python_client.models import Post


class PostApiTest(IntegrationTestCase):

    def setUp(self):
        super().setUp()

        self.api = PostApi(self.config)
        post = Post(Post.hash_identifier('test1as1' + str(datetime.today().timestamp())))
        post.source = 'test_tesa_lies'
        post.slug = 'ttttt-sss'
        post.title = 'Test 123'

        r = self.api.create(post, True)
        self.post, status, headers = r.get()

    def test_create(self):
        post = Post(Post.hash_identifier(str(datetime.today().isoformat())))
        post.source = 'test_tesa_lies'
        post.slug = 'ttttt-sss'
        post.title = 'Test 123'
        post.description = 'a test description'
        post.tags = ['test', 'lok']
        post.path = ['test1', 'test3', 'tank']
        post.release = datetime.today()
        post.listing = True
        author = Author()
        author.email = 'felix@felix-scholz.org'
        author.name = 'Felix Scholz'
        post.author.append(author)
        post.acl.group.append('test_123')
        post.acl.user.append('tester')
        post.images.append(self.generate_test_image())
        post.images.append(self.generate_test_image())
        post.images.append(self.generate_test_image())
        post.preview.append(self.generate_test_image())
        post.preview.append(self.generate_test_image())
        post.src = self.generate_test_markdown()

        r = self.api.create(post, True)
        post, status, headers = r.get()
        pprint(post)

        self.assertEqual(200, status)

    def test_show(self):
        r = self.api.show(Post.hash_identifier('test3'), True, True, True, True)
        post, status, headers = r.get()
        pprint(post)

        self.assertEqual(200, status)

    def test_delete(self):
        r = self.api.delete(Post.hash_identifier('test3'), False, True)
        post, status, headers = r.get()
        pprint(post)

        self.assertEqual(200, status)

    def test_update(self):
        identifier = Post.hash_identifier('test1')
        r = self.api.show(identifier, True, True, True, True)
        post, status, headers = r.get()
        pprint(post)

        post.description = 'updated description'
        #post.images.append('/tmp/blog/5a84aadebdcea434049969.png')

        r = self.api.update(post, ['description'], True)
        post, status, headers = r.get()
        pprint(post)

        self.assertEqual(200, status)

    def test_list(self):
        response, status, headers = self.api.list()
        pprint(response)

        self.assertEqual(200, status)


if __name__ == '__main__':
    unittest_main()
