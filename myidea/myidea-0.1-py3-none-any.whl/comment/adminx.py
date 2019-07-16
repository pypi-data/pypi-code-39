from django.contrib import admin

import xadmin
from xadmin.layout import Row, Fieldset

from .models import Comment
from myidea.base_admin import BaseOwnerAdmin
# Register your models here.


@xadmin.sites.register(Comment)
class CommentAdmin:
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
