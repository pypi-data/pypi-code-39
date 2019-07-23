from django.conf.urls import include, url
from cssocialprofile.views import index
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from cssocialprofile.views import edit_profile
from cssocialprofile.views import edit_profile_photo
from cssocialprofile.views import edit_profile_social

# default view for our index
urlpatterns = [url(r"^$", views.index, name="cssocialprofile_index")]

urlpatterns = [
    url(r'^$', index, name="cssocialprofile_index"),
]

# register and social urls
urlpatterns += [
    url(r'^logout$', LogoutView.as_view(), name='cssocialprofile_logout'),
    url(r'^login$', LoginView.as_view(), name='cssocialprofile_user_login'),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^social/', include('social_django.urls', namespace='social'))
]

# default profile edit urls
urlpatterns += [
    url(r'^edit-profile$', edit_profile, name='cssocialprofile_edit_profile'),
    url(r'^edit-profile-photo$', edit_profile_photo, name='cssocialprofile_edit_profile_photo'),
    url(r'^edit-profile-social$', edit_profile_social, name='cssocialprofile_edit_profile_social'),
]
