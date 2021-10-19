from django.db import models
from CustomUser.models import CustomUser


FORM_STATUS = ( 
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
)

MENU_CHOICE = (
    ("Vegetarian", "vegetarian"),
    ("Non-Vegetarian", "Non-Vegetarian"),
    ("Dessert", "Dessert"),
    ("Breakfast", "Breakfast"),
    ("Sweet", "Sweet"),
)

# Create your models here.
class Hotel_Form(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    pincode = models.IntegerField()
    cuisine = models.CharField(max_length=100)
    cost = models.IntegerField()
    serving_form = models.TimeField()
    serving_till = models.TimeField()
    delivery = models.CharField(max_length=10)
    loc = models.CharField(max_length=100)
    open_status = models.CharField(max_length=50)
    img1 = models.ImageField(upload_to = "Restaurant")
    img2 = models.ImageField(upload_to = "Locality")
    status = models.CharField(
        choices=FORM_STATUS, max_length=30, default=FORM_STATUS[0][0])

class Hotel(models.Model):
    name = models.CharField(max_length=50)
    registation_form = models.ForeignKey(Hotel_Form, on_delete=models.CASCADE) 
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    image = models.ImageField(upload_to="hotel_image")
    hotel_number = models.IntegerField()
    hotel_email = models.CharField(max_length=50)
    shop_license_number = models.IntegerField(blank=True, null=True)
    fssai_number = models.IntegerField(blank=True, null=True)
    fssai_image = models.FileField(upload_to = "fssai", blank=True, null=True)

    def __str__(self):
        return self.name

class Hotel_Image(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    hotel_image = models.ImageField(upload_to="hotel_image", blank=False, null=False)

class Menu(models.Model):
    hotel = models.ForeignKey(Hotel, models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="menu")
    food_type = models.CharField(max_length=20, choices=MENU_CHOICE)

    def __str__(self):
        return self.name

class Menu_Image(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    more_image = models.ImageField(upload_to="menu")