# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list_view, name='stories'), # /community/
    path('share/', views.share_story_view, name='share_story'), # /community/share/
]