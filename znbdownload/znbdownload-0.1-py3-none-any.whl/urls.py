# from django.conf.urls import url
from django.urls import path

from . import views

"""
Build links like this:
<a href="{% url 'znbdownload:secret_file_link' id=object.id %}">Download</a>
"""

app_name = 'znbdownload'
urlpatterns = [
    path('<int:id>/', views.SecretFileView.as_view(), name='secret_file'),
    path('<int:id>/secret', views.SecretFileLinkView.as_view(), name='secret_file_link'),
]
