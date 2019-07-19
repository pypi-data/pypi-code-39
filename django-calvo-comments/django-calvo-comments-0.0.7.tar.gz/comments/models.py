from django.db import models

from django.conf import settings
from django.db import models
from django.utils import timezone

# comments via urls and users

class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,on_delete=models.CASCADE)
    url         = models.URLField() 
    content     = models.TextField()
    #image       = models.ImageField()
    allow_annon = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


    @property
    def owner(self):
        return self.user


class Post(models.Model):
    content = models.TextField()

    def get_excerpt(self, char):
        return self.content[:char]


class CommentPost(models.Model):
    """
    model Post
    """
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


