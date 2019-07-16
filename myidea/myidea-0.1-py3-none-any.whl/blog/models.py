from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from django.core.cache import cache

import mistune

# Create your models here.


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        {STATUS_NORMAL, 'normal'},
        {STATUS_DELETE, 'delete'},
    )

    name = models.CharField(max_length=50, verbose_name='category name')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='status')
    is_nav = models.BooleanField(default=False, verbose_name='is nav')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created time')

    class Meta:
        verbose_name = verbose_name_plural = 'category'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        {STATUS_NORMAL, 'normal'},
        {STATUS_DELETE, 'delete'},
    )

    name = models.CharField(max_length=10, verbose_name='tag name')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='status')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created time')

    class Meta:
        verbose_name = verbose_name_plural = 'tag'

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        {STATUS_NORMAL, 'normal'},
        {STATUS_DELETE, 'delete'},
        {STATUS_DRAFT, 'draft'},
    )

    title = models.CharField(max_length=255, verbose_name='title')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='descriptions')
    content = models.TextField(verbose_name='content', help_text='the post must be MarkDown format')
    content_html = models.TextField(verbose_name='content html code', blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='status')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='tag')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='created time')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    is_md = models.BooleanField(default=False, verbose_name='markdown enable')

    class Meta:
        verbose_name = verbose_name_plural = 'post'
        ordering = ['-id']

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')

        return post_list, tag

    # @cached_property
    # def tags(self):
    #     # return ','.join(self.tag.values_list('name', flat=False))
    #     return ','.join(self.tag.objects.filter(status=Tag.STATUS_NORMAL))

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')

        return post_list, category

    @classmethod
    def latest_posts(cls, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        if with_related:
            queryset = queryset.select_related('owner', 'category')
        return queryset

    @classmethod
    def hot_posts(cls):
        result = cache.get('host_posts')
        if not result:
            result = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
            cache.set('host_posts', result, 10 * 60)
        return result

    def save(self, *args, **kwargs):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
        super().save(*args, **kwargs)
