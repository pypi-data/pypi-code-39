from django.urls import path

from . import views

app_name = "cas"

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("users/language", views.language, name="language"),
    path("enviroment", views.enviroment, name="enviroment"),
]
