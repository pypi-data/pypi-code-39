from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'notify/$', views.NotifyView, name='notify'),
]
