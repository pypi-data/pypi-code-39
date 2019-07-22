from django.shortcuts import render
from django.http import HttpResponse

from hello.forms import ProjectForm

from hello.models import Project


# Create your views here.


def hello_world(request, *args, **kwargs):
    # return HttpResponse("<h1>hello world</h1>")
    return render(request, "hello_world.html", {})


def contact_views(request, *args, **kwargs):
    return render(request, "contact.html", {})


def project_views(request):
    context = {}
    context["objects"] = Project.objects.all()
    return render(request, "project/project.html", context)


def project_create_view(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProjectForm()
    context = {"form": form}
    return render(request, "project/project_create.html", context)
