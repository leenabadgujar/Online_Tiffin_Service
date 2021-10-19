from django.contrib import admin
from food.models import Application_Form, Cart, Payment, Rating, Order, Payment

# Register your models here.
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(Application_Form)
admin.site.register(Order)
admin.site.register(Payment)
