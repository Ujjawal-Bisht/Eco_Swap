from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list_view, name='item_list'), 
    path('home/', views.home_view, name='home'),
    path('add/', views.add_item_view, name='add_item'),
    path('item/<int:pk>/', views.item_detail_view, name='item_detail'),
    path('my-listings/', views.my_listings_view, name='my_listings'),
    path('item/delete/<int:pk>/', views.delete_item_view, name='delete_item'),
    path('item/<int:item_id>/request/', views.send_swap_request, name='send_swap_request'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('request/<int:req_id>/<str:new_status>/', views.update_request_status, name='update_status'),
]