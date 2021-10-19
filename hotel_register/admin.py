from hotel_register.forms import Add_Menu
from hotel_register.views import add_menu
from django.contrib import admin
from .models import Hotel, Hotel_Form, Hotel_Image, Menu, Menu_Image

# Register your models here.
admin.site.register(Hotel_Form)
admin.site.register(Hotel)
admin.site.register(Hotel_Image)
admin.site.register(Menu)
admin.site.register(Menu_Image)