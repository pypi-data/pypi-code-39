from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls')),
    path('users/rest-auth/', include('rest_auth.urls')),
]
