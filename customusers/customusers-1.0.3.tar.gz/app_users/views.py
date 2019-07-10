from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm

from rest_framework import generics
from . import models
from . import serializers

class signup(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UserListView(generics.ListCreateAPIView):
	queryset = models.CustomUser.objects.all()
	serializer_class = serializers.UserSerializer