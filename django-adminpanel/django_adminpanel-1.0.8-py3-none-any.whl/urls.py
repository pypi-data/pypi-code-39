"""project URL Configuration
For Backend
"""
from django.conf import settings as setting
from django.conf.urls.static import static
from django.urls import path
from .views import *
urlpatterns = [
     path('blogs', apblogs_blogs_list,name='apblogs_blogs_list'),
     path('blogs/add-new', apblogs_add_blog,name='apblogs_add_blog'),
     path('blogs/submit', apblogs_submit_blog,name='apblogs_submit_blog'),
     #Tags url
	 path('blogs/tags', apblogs_tags_list,name='apblogs_tags_list'),
     path('blogs/tags/edit/<id>', apblogs_edit_tags,name='apblogs_edit_tags'),
     path('blogs/tags/submit', apblogs_tags_submit,name='apblogs_tags_submit'),
     path('blogs/tags/update', apblogs_tags_update,name='apblogs_tags_update'),
     path('blogs/tags/delete', apblogs_tags_delete,name='apblogs_tags_delete'),
	 #Category url
	 path('blogs/category', apblogs_category_list,name='apblogs_category_list'),
     path('blogs/category/edit/<id>', apblogs_edit_category,name='apblogs_edit_category'),
     path('blogs/category/submit', apblogs_category_submit,name='apblogs_category_submit'),
     path('blogs/category/update', apblogs_category_update,name='apblogs_category_update'),
     path('blogs/category/delete', apblogs_category_delete,name='apblogs_category_delete'),	
]
urlpatterns += static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)