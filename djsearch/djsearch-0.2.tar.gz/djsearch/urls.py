from django.urls import path

from .views import search

app_name = 'django_search_models'

urlpatterns = [
    path('', search, name='search'),
]
