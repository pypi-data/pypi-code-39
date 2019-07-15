# from django.views.generic import TemplateView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import JobPosting


class JobPostingDetail(DetailView):
    model = JobPosting


class JobPostingList(ListView):
    model = JobPosting

    def get_queryset(self):
        queryset = self.model.objects.all().filter(active=True)
        return queryset
