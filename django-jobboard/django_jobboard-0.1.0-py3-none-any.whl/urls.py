from django.urls import path

from jobboard import views

urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
    path("postings/", views.JobPostingList.as_view(), name="jobposting_list"),
    path("posting/<slug:slug>/", views.JobPostingDetail.as_view(), name="jobposting_detail"),
]
