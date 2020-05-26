from django.shortcuts import render, get_object_or_404
from .models import post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from django.contrib.auth.models import User


def home(request):
    post_list = post.objects.all().order_by('-date_posted')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    avg = post.objects.aggregate(avg_rating=Avg('rating'))
    count = post.objects.count()
    total_rating1 = post.objects.filter(rating=1).count()
    total_rating2 = post.objects.filter(rating=2).count()
    total_rating3 = post.objects.filter(rating=3).count()
    total_rating4 = post.objects.filter(rating=4).count()
    total_rating5 = post.objects.filter(rating=5).count()

    context = {
        'posts': posts,  # pass in posts dict to 'posts' key in context dict
        'avg': avg,
        'total_posts': count,
        'total_rating1': total_rating1,
        'total_rating2': total_rating2,
        'total_rating3': total_rating3,
        'total_rating4': total_rating4,
        'total_rating5': total_rating5
    }

    return render(request, 'blog/home.html', context)  # pass in the context dict


class PostListView(ListView):  # <app>/<model>_<Viewtype>.html
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10  # number of posts per page


class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['rating', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserPostListView(ListView):  # <app>/<model>_<Viewtype>.html
    model = post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = post
    fields = ['rating', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
