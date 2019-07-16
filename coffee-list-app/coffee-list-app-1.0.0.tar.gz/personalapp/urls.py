"""personal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')ococ
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from hello.views import hello_world, contact_views, project_views, project_create_view
def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", hello_world, name="home"),
    path("contact/", contact_views, name="contact"),
    path("project/", project_views, name="project"),
    path("create/", project_create_view, name="create"),
    path('', include('django_prometheus.urls')),
    path('sentry-debug/', trigger_error),
] 