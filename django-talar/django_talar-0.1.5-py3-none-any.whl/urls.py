from django.conf.urls import path

from . import views


urlpatterns = [
    path('notify/', views.NotifyView, name='notify'),
]
