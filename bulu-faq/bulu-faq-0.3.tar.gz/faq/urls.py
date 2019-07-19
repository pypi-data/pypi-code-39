from django.conf import settings
try:
    from django.urls import include, path
except ImportError:
    from django.conf.urls import include, url as path

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()


router.register('faqs', views.FAQViewSet, 'api-faq')
router.register('', views.FAQCategoryViewSet, 'api-category')


urlpatterns = [
    path('', include(router.urls))
]
