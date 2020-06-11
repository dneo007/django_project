from django.shortcuts import render, get_object_or_404
from .models import post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from django.contrib.auth.models import User
from users.models import Profile


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

    average = post.objects.aggregate(avg_rating=Avg('rating'))
    print(average)
    avg = 0
    if average['avg_rating'] is not None:
        avg = round(average['avg_rating'], 2)
    count = post.objects.count()
    total_rating1 = post.objects.filter(rating=1).count()
    total_rating2 = post.objects.filter(rating=2).count()
    total_rating3 = post.objects.filter(rating=3).count()
    total_rating4 = post.objects.filter(rating=4).count()
    total_rating5 = post.objects.filter(rating=5).count()

    numlist = [total_rating1, total_rating2, total_rating3, total_rating4, total_rating5]
    largest = max(numlist)

    currentUser = request.user.username

    context = {
        'posts': posts,  # pass in posts dict to 'posts' key in context dict
        'avg': avg,
        'total_posts': count,
        'total_rating1': total_rating1,
        'total_rating2': total_rating2,
        'total_rating3': total_rating3,
        'total_rating4': total_rating4,
        'total_rating5': total_rating5,
        'largest': largest,
        'currentUser': currentUser
    }

    return render(request, 'blog/home.html', context)  # pass in the context dict


class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['rating', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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


class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


def usersProfile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    pic = profile.image
    context = {'profilePic': pic,
               'user': user,
               }
    return render(request, 'blog/users_profile.html', context)


def usersPosts(request, username):
    user = User.objects.get(username=username)
    posts = post.objects.filter(author=user).order_by('-date_posted')
    context = {'posts': posts,
               'username': username,
               }
    return render(request, 'blog/users_posts.html', context)
