from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('', views.post_list, name='post_list'),
    url('post/<int:pk>/', views.post_detail, name='post_detail'),
    url('post/new', views.post_new, name='post_new'),
    url('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]