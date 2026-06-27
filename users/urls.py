# pyrefly: ignore [missing-import]
from django.urls import path
# pyrefly: ignore [missing-import]
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('login'), name='users_root'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]