from django.db import models
from CustomUser.models import CustomUser

FORM_STATUS = (  # copy this
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
)

# Create your models here.
class Delivery_Form(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    pincode = models.IntegerField()
    experience = models.CharField(max_length=10)
    licenses = models.CharField(max_length=10)
    working_form = models.TimeField()
    working_to = models.TimeField()
    weekends = models.CharField(max_length=10)
    money = models.DecimalField(max_digits=5, decimal_places=2)
    range_of_delivery = models.DecimalField(max_digits=5, decimal_places=2)
    vehicle = models.CharField(max_length=10)
    status = models.CharField(
        choices=FORM_STATUS, max_length=30, default=FORM_STATUS[0][0])


class Delivery(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    pincode = models.IntegerField()
    working_form = models.TimeField()
    working_to = models.TimeField()
    money = models.DecimalField(max_digits=5, decimal_places=2)
    range_of_delivery = models.DecimalField(max_digits=5, decimal_places=2)
    vehicle = models.CharField(max_length=10)
    image = models.ImageField(upload_to="Delivery")
    aadhar_card_image = models.ImageField(
        upload_to="Delivery/aadhar_card", default="", blank=False, null=False)
    driving_licence_image = models.ImageField(
        upload_to="Delivery/driving_licence", default="", blank=False, null=False)


class Delivery_payment(models.Model):
    order_id = models.CharField(max_length=50, null=False)
    payment_id = models.CharField(max_length=50, null=True, blank=True)
    application_Form = models.ForeignKey(to='food.Application_Form', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
