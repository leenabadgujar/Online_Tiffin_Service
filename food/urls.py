from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('join_us/', views.join_us, name="join_us"),
    path('hotel_detail/<int:hotel_id>/',
         views.hotel_detail, name="hotel_detail"),
    path('hotel_detail/<int:hotel_id>/<slug:extra>/',
         views.hotel_detail, name="hotel_detail"),
    path('cart/', views.my_cart, name="my_cart"),
    path('cart/plus', views.plus_cart, name="plus_cart"),
    path('cart/minus', views.minus_cart, name="minus_cart"),
    path('verify_payment/', views.verifyPayment, name='verify_payment'),
    path('order/', views.orders, name="order"),
    path('search/', views.search_items, name="search"),
    path('all_hotel/', views.all_hotel, name="all_hotel"),
    path('all_menu/', views.all_menu, name="all_menu"),
]
