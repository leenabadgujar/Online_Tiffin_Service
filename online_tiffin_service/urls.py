from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('food.urls')),
    path('user/', include('CustomUser.urls')),
    path('delivery_boy/', include('delivery_boy.urls')),
    path('hotel/', include('hotel_register.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)