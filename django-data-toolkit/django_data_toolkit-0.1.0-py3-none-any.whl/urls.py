from django.urls import path

from datatoolkit import views

urlpatterns = [
    path("", views.DataToolkitIndexView.as_view(), name="datatoolkit_index"),
]
