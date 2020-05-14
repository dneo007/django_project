from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.setupFaceID, name='setup'),
    path('setupSuccess/', views.setupSuccess, name='success'),
    ]
