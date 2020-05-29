from django.urls import path
from .views import PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('user-profile/<str:username>', views.usersProfile, name='users-profile'),
    path('users-posts/<str:username>', views.usersPosts, name='users-posts'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
]
