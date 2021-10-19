from django.urls import path
from . import views

urlpatterns = [
    path('application/', views.hotel_register_form, name='hotel_register_form'),
    path('add/', views.add_hotel, name='add_hotel'),
    path('<int:hotel_id>/menu/add/', views.add_menu, name="add_menu"),
    path('<int:menu_id>/menu/update/', views.update_menu, name="update_menu"),
    path('<int:hotel_id>/', views.hotel_details, name="hotel_details"),
    path('<int:hotel_id>/update/', views.update_hotel, name="update_hotel"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('all/', views.owner_hotels, name="owner_hotel"),
    path('orders/', views.owner_orders, name="owner_orders"),
    path('menu_items/', views.owner_menu_items, name="owner_menu_items"),
    path('hotel_feedback/', views.hotel_feedback, name="hotel_feedback"),
]