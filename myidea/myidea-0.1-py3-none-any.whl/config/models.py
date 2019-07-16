from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
# Create your models here.


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        {STATUS_NORMAL, 'normal'},
        {STATUS_DELETE, 'delete'},
    )

    title = models.CharField(max_length=50, verbose_name='title')
    href = models.URLField(verbose_name='link')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='status')
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6), range(1, 6)), verbose_name='weight',
                                         help_text='weight order from high to low')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created time')

    class Meta:
        verbose_name = verbose_name_plural = 'Link'


class SideBar(models.Model):
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
        {DISPLAY_HTML, 'HTML'},
        {DISPLAY_LATEST, 'Latest Posts'},
        {DISPLAY_HOT, 'Hottest Posts'},
        {DISPLAY_COMMENT, 'Latest Comments'},
    )
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        {STATUS_SHOW, 'show'},
        {STATUS_HIDE, 'hide'},
    )

    title = models.CharField(max_length=50, verbose_name='title')
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name='display type')
    content = models.CharField(max_length=500, blank=True, verbose_name='post')
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name='status')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created time')

    class Meta:
        verbose_name = verbose_name_plural = 'side bar'

    @classmethod
    def get_all(cls):
        # import time
        # time.sleep(3)
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        """直接渲染模板"""
        from blog.models import Post
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                'posts': Post.latest_posts(with_related=False)
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': Post.hot_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL)
            }
            result = render_to_string('config/blocks/sidebar_comments.html', context)
        return result
