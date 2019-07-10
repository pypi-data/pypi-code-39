from django.urls import path
from .views import signup

from . import views

urlpatterns = [
	path('signup/', signup.as_view(), name='signup'),
	path('', views.UserListView.as_view()),
]