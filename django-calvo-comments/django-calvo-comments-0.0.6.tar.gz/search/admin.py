from django.contrib import admin

# Register your models here.

from search.models import *

from .models import Post


admin.site.register(Post)
