from django.urls import path
from . import views

urlpatterns = [
    path('', views.delivery_boy_dashboard, name="delivery_boy_dashboard"),
    path('form/', views.delivery_boy_form, name='delivery_boy_from'),
    path('add/', views.add_information, name="add_delivery_boy"),
    path('book_delivery_boy/', views.book_delivery_boy, name="book_delivery_boy"),
    path('verify_payment/', views.verifyPayment, name='verify_payment'),
    path('pending/', views.pending, name='pending'),
    path('accepted/', views.accepted, name='accepted'),
    path('rejected/', views.rejected, name='rejected'),
]
