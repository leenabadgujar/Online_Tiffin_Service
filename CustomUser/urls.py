from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.registration, name="registration"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.userlogout, name="logout"),
    path('token', views.token_send, name="token_send"),
    path('success', views.success, name='success'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('error', views.error_page, name='error')
    # path('profile/', views.userprofile, name="profile"),
    # path('changepassword/', views.changepassword, name="changepassword"),
]
