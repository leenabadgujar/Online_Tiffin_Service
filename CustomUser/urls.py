from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.registration, name="registration"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.userlogout, name="logout"),
    # path('profile/', views.userprofile, name="profile"),
    # path('changepassword/', views.changepassword, name="changepassword"),
]