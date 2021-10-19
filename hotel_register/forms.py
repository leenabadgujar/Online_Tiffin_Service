from django import forms
from django.db.models import fields
from .models import Hotel, Menu

class Add_Hotel(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = "__all__"
        labels = {"name":"Hotel Name", "address": "Hotel Address", "hotel_number": "Hotel Mobile Number", "image" : "Hotel Image"}

class Add_Menu(forms.ModelForm):
    class Meta:
        model = Menu
        fields = "__all__"