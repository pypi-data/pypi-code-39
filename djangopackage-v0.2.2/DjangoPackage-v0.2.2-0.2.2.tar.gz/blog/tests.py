from django.test import TestCase, RequestFactory
from .models import Post, Comment, Category
from django.utils import timezone
from .views import blog_category as bc
from .views import blog_detail as bd
from .forms import CommentForm
from .apps import BlogConfig
from django.apps import apps
from django.urls import reverse
from .forms import CommentForm
from model_mommy import mommy

# Create your tests here.


class ModelTestMommy(TestCase):

    def test_category_model_mommy(self):
        cat = mommy.make(Category)
        self.assertTrue(isinstance(cat, Category))
        self.assertEqual(cat.category(), cat.name)

    def test_post_title_model_mommy(self):
        tit = mommy.make(Post)
        self.assertTrue(isinstance(tit, Post))
        self.assertEqual(tit.post_title(), tit.title)

    def test_post_body_mommy(self):
        bod = mommy.make(Post)
        self.assertTrue(isinstance(bod, Post))
        self.assertEqual(bod.post_body(), bod.body)

    def test_post_created_on_mommy(self):
        con = mommy.make(Post)
        self.assertTrue(isinstance(con, Post))
        self.assertEqual(con.post_created_on(), con.created_on)

    def test_post_last_modified_on_mommy(self):
        lon = mommy.make(Post)
        self.assertTrue(isinstance(lon, Post))
        self.assertEqual(lon.post_last_modified(), lon.last_modified)

    def test_post_categories_mommy(self):
        catp = mommy.make(Post)
        self.assertTrue(isinstance(catp, Post))
        self.assertEqual(catp.post_categories(), catp.categories)

    def test_comment_author_mommy(self):
        com = mommy.make(Comment)
        self.assertTrue(isinstance(com, Comment))
        self.assertEqual(com.comment_author(), com.author)

    def test_comment_body_mommy(self):
        comb = mommy.make(Comment)
        self.assertTrue(isinstance(comb, Comment))
        self.assertEqual(comb.comment_body(), comb.body)

    def test_comment_created_on_mommy(self):
        crtdon = mommy.make(Comment)
        self.assertTrue(isinstance(crtdon, Comment))
        self.assertEqual(crtdon.comment_created_on(), crtdon.created_on)

    def test_comment_post_mommy(self):
        cpost = mommy.make(Comment)
        self.assertTrue(isinstance(cpost, Comment))
        self.assertEqual(cpost.comment_post(), cpost.post)

    def test_blog_index_view_uses_correct_template(self):
        response = self.client.get(reverse('blog_index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_index.html')


class TestApps(TestCase):
    """docstring for TestApps"""

    def test_apps(self):
        self.assertEqual(BlogConfig.name, "blog")
        self.assertEqual(apps.get_app_config("blog").name, "blog")


class TestingTemplate(TestCase):
    """docstring for TestingTemplate"""

    def create_post(self, ptitle="only a test", pbody="yes, this is only a test", pcrtdon=timezone.now(), plastmdfd=timezone.now()):
        return Post.objects.create(title=ptitle, body=pbody, created_on=pcrtdon, last_modified=plastmdfd)

    def test_project_category_view_uses_correct_template(self):
        self.factory = RequestFactory()
        self.cv = self.create_post()
        request = self.factory.get("<category>/")
        request.cv = self.cv
        response = bc(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_project_detail_view_uses_correct_template(self):
        self.factory = RequestFactory()
        self.dv = self.create_post()
        request = self.factory.get("<int:pk>/")
        request.dv = self.dv
        response = bd(request, 1)
        self.assertEqual(response.status_code, 200)
