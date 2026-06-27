# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

app_name = 'centers' 

urlpatterns = [
    path('map/', views.center_map_view, name='map_view'),
]