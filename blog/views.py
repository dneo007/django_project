import shutil

from django.shortcuts import render, get_object_or_404
from .models import post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['content']


def showProducts(request):
    return render(request, 'blog/products.html')


# fCreate your views here.
def home(request):
    form = PostForm(request.POST)
    post_list = post.objects.all().order_by('-date_posted')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = request.user
            form.save()

    context = {
        'posts': posts  # pass in posts dict to 'posts' key in context dict
        , 'form': form
    }

    return render(request, 'blog/home.html', context)  # pass in the context dict


class PostListView(ListView):  # <app>/<model>_<Viewtype>.html
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10  # number of posts per page


class UserPostListView(ListView):  # <app>/<model>_<Viewtype>.html
    model = post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
