from django.urls import path
from . import views

app_name = 'chat' 

urlpatterns = [
    path('<int:swap_id>/', views.chat_room, name='chat_room'),
    path('api/unread-total/', views.api_unread_count, name='api_unread_count'),
    path('api/unread-counts/', views.get_unread_counts, name='get_unread_counts'),
]