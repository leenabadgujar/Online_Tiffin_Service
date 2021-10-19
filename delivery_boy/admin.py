from delivery_boy.models import Delivery, Delivery_Form, Delivery_payment
from django.contrib import admin

# Register your models here.
admin.site.register(Delivery_Form)
admin.site.register(Delivery)
admin.site.register(Delivery_payment)
