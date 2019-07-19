from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, CommentPost
from .forms import PostForm, CommentPostForm

# Create your views here.


class HomeView(TemplateView):
    template_name = 'comments/home.html'




def post_list(request):
    posts = CommentPost.objects.filter(published_date__lte=timezone.now()).order_by(
        'published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = CommentPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentPostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentPostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# class AdminView(TemplateView):
#     template_name = 'employee/admin.html'

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(AdminView, self).dispatch(request,*args,*kwargs)

    
# class PostUpdateView(UpdateView):
#     model = models.Post
#     form_class = forms.PostForm
#     success_url = '/'

#     def post(self, request, *args, **kwargs):
#         if getattr(request.user, 'first_name', None) == 'Martin':
#             raise Http404()
#         return super(PostUpdateView, self).post(request, *args, **kwargs)
