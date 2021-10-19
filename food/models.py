from django.db.models.fields import CharField
from delivery_boy.models import Delivery
from django.db import models
from hotel_register.models import Hotel, Menu
from CustomUser.models import CustomUser
from datetime import date

FORM_STATUS = (
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
)

# Create your models here.
class Rating(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.FloatField()
    review = models.TextField()
    is_verified = models.BooleanField(default=True)


class Cart(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(Menu)
    order_from = models.DateField(null=True, blank=True)
    order_till = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)
    quantity = models.CharField(max_length=1000000, default="")
    price = models.IntegerField(default=0)

class Payment(models.Model):
    order_id = models.CharField(max_length=50, null=False)
    payment_id = models.CharField(max_length=50, null=True, blank=True)
    menu_details = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

class Application_Form(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delivery_boy = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    apply_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=FORM_STATUS, max_length=30, default=FORM_STATUS[0][0])
    delivery_time = models.TimeField()
    delivery_start = models.DateField(default=date.today)
    delivery_end = models.DateField(default=date.today)
    pickup_address = models.TextField(max_length=1000, default="")
    delivery_address = models.TextField(max_length=1000, default="")