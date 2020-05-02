from django.urls import path
from .views import PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
]
