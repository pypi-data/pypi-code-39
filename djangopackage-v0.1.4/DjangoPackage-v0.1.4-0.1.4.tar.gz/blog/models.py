from django.db import models

from django_prometheus.models import ExportModelOperationsMixin

# Monitoring your models -- 'ExportModelOperationsMixin'


class Category(ExportModelOperationsMixin('category'), models.Model):
    name = models.CharField(max_length=20)

    def category(self):
        return self.name


class Post(ExportModelOperationsMixin('post'), models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")

    def post_title(self):
        return self.title

    def post_body(self):
        return self.body

    def post_created_on(self):
        return self.created_on

    def post_last_modified(self):
        return self.last_modified

    def post_categories(self):
        return self.categories


class Comment(ExportModelOperationsMixin('comment'), models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def comment_author(self):
        return self.author

    def comment_body(self):
        return self.body

    def comment_created_on(self):
        return self.created_on

    def comment_post(self):
        return self.post
