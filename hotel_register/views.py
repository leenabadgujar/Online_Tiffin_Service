from food.models import Order, Rating
from hotel_register.forms import Add_Hotel, Add_Menu
from delivery_boy.models import Delivery_Form
from django.contrib import messages
from django.db import models
from hotel_register.models import Hotel, Hotel_Form, Hotel_Image, Menu, Menu_Image
from django.shortcuts import redirect, render
from django.forms.models import inlineformset_factory

# Create your views here.
def hotel_register_form(request):
    if request.user:
        if request.method == "POST":
            address = request.POST['address']
            city = request.POST['city']
            code = request.POST['code']
            cuisine = request.POST['cuisine']
            cost = request.POST['cost']
            serving_form = request.POST['from']
            serving_till = request.POST['till']
            delivery = request.POST['delivery']
            loc = request.POST['loc']
            open_status = request.POST['open_status']
            img1 = request.FILES['img1']
            img2 = request.FILES['img2']
            Hotel_Form(customer=request.user, address=address, city=city, pincode=code, cuisine=cuisine, cost=cost, serving_form=serving_form, serving_till=serving_till, delivery=delivery, loc=loc, open_status=open_status, img1=img1, img2=img2).save()
            messages.success(request, "Form submitted successfully.")
            return redirect('home')

        try:
            delivery_form = Delivery_Form.objects.get(customer=request.user)
            if delivery_form.status == "Pending":
                messages.info(request, 'Your application for delivery boy is pending.')
                return redirect('home')
            elif delivery_form.status == "Accepted":
                messages.error(request, 'Your are hotel owner.')
                return redirect('home')
            else:
                return render(request, 'hotel_register/hotel_register.html')

        except:
            try:
                hotel_form = Hotel_Form.objects.get(customer=request.user)
                if hotel_form.status == "Rejected":
                    messages.error(request, 'Your application has been rejected.')
                    return redirect('home')

                elif hotel_form.status == "Pending":
                    messages.info(request, 'Your application is pending.')
                    return redirect('home')

                else:
                    return redirect('add_hotel')

            except:
                return render(request, 'hotel_register/hotel_register.html')

    return redirect('login')

def add_hotel(request):
    if request.user:
        ImageFormSet = inlineformset_factory(Hotel, Hotel_Image, fields=("hotel_image",), extra=5)
        if request.method == "POST":
            add_hotel_form = Add_Hotel(request.POST, request.FILES)
            image_form = ImageFormSet(request.POST, request.FILES)
            
            if all([add_hotel_form.is_valid(), image_form.is_valid()]):
                hotel_form = add_hotel_form.save()
                for field in image_form:
                    if field.is_valid():
                        if field.cleaned_data:
                            field_form = field.save(commit=False)
                            field_form.hotel = hotel_form
                            field_form.save()
                messages.success(request, "Form Submitted successfully.")
                return redirect('dashboard')
            messages.error(request, "Something wen't wrong.")
            return redirect('home')

        try: 
            verify = Hotel_Form.objects.get(customer=request.user)
            
        except:
            verify = False

        if verify:
            if verify.status == "Rejected":
                messages.error(request, "Your application has been rejected.")
                return redirect("home")

            elif verify.status == "Pending":
                messages.info(request, "Your application is pending.")
                return redirect("home")

            else:
                add_hotel_form = Add_Hotel(initial={"registation_form":verify})
                image_form = ImageFormSet()
                return render(request, 'hotel_register/add_hotel.html', {"application_form": verify, "add_hotel_form": add_hotel_form, "image_form": image_form})

        else:
            messages.error(request, "Your are not apply for hotel owner on our site.")
            return redirect("home")

    return redirect('login')

def update_hotel(request, hotel_id):
    if request.user:
        hotel = Hotel.objects.get(id=hotel_id)
        ImageFormSet = inlineformset_factory(Hotel, Hotel_Image, fields=("hotel_image",), extra=1)
        if request.method == "POST":
            add_hotel_form = Add_Hotel(request.POST, request.FILES, instance=hotel)
            image_form = ImageFormSet(request.POST, request.FILES, instance=hotel)
            
            if all([add_hotel_form.is_valid(), image_form.is_valid()]):
                hotel_form = add_hotel_form.save()
                for field in image_form:
                    if field.is_valid():
                        if field.cleaned_data:
                            field_form = field.save(commit=False)
                            field_form.hotel = hotel_form
                            field_form.save()

                messages.success(request, "Form Submitted successfully.")
                return redirect('hotel_details', hotel_id=hotel_id)
            messages.error(request, "Something wen't wrong.")
            return redirect('home')

        try: 
            verify = Hotel_Form.objects.get(customer=request.user)
            
        except:
            verify = False

        if verify:
            if verify.status == "Rejected":
                messages.error(request, "Your application has been rejected.")
                return redirect("home")

            elif verify.status == "Pending":
                messages.info(request, "Your application is pending.")
                return redirect("home")

            else:
                add_hotel_form = Add_Hotel(instance=hotel)
                image_form = ImageFormSet(instance=hotel)
                return render(request, 'hotel_register/add_hotel.html', {"application_form": verify, "add_hotel_form": add_hotel_form, "image_form": image_form})

        else:
            messages.error(request, "Your are not apply for hotel owner on our site.")
            return redirect("home")

    return redirect('login')

def add_menu(request, hotel_id):
    if request.user:
        ImageFormSet = inlineformset_factory(Menu, Menu_Image, fields=("more_image",), extra=5)
        try:
            verify = Hotel.objects.get(id = hotel_id)
        except:
            verify = False

        if request.method == "POST":
            menu_form = Add_Menu(request.POST, request.FILES)
            image_form = ImageFormSet(request.POST, request.FILES)
            
            if all([menu_form.is_valid(), image_form.is_valid()]):
                nemu_form = menu_form.save()
                for field in image_form:
                    if field.is_valid():
                        if field.cleaned_data:
                            field_form = field.save(commit=False)
                            field_form.menu = nemu_form
                            field_form.save()
                            
                messages.success(request, "Menu Add Successfully.")
                return redirect("hotel_details", verify.id)

            messages.error(request, "Something wen't wrong.")
            return redirect('home')    

        if verify:
            form = Add_Menu(initial={"hotel":verify})
            image_form = ImageFormSet()
            return render(request, "hotel_register/add_menu.html",{"form": form, "image_form" : image_form})

        else:
            messages.error(request, "Your are not hotel owner.")
            return redirect("home")

    return redirect('login')
  
def update_menu(request, menu_id):
    if request.user:
        menu = Menu.objects.get(id=menu_id)
        ImageFormSet = inlineformset_factory(Menu, Menu_Image, fields=("more_image",), extra=1)

        if request.method == "POST":
            menu_form = Add_Menu(request.POST, request.FILES, instance=menu)
            image_form = ImageFormSet(request.POST, request.FILES, instance=menu)
            
            if all([menu_form.is_valid(), image_form.is_valid()]):
                nemu_form = menu_form.save()
                for field in image_form:
                    if field.is_valid():
                        if field.cleaned_data:
                            field_form = field.save(commit=False)
                            field_form.menu = nemu_form
                            field_form.save()
                            
                messages.success(request, "Menu Updated Successfully.")
                return redirect("dashboard")

            messages.error(request, "Something wen't wrong.")
            return redirect('home')    

        form = Add_Menu(instance=menu)
        image_form = ImageFormSet(instance=menu)
        return render(request, "hotel_register/add_menu.html",{"form": form, "image_form" : image_form})

    return redirect('login')

def hotel_details(request, hotel_id):
    hotel_form = Hotel_Form.objects.get(customer=request.user)
    hotel = Hotel.objects.get(id=hotel_id)
    if hotel.registation_form.customer == request.user:
        menu_items = Menu.objects.filter(hotel=hotel)
        
        return render(request, 'hotel_register/hotel_details.html', {"hotel":hotel,"menu_items": menu_items})
    else:
        messages.error(request, "You are not owner of this hotel")
        return redirect('home')

def dashboard(request):
    if request.user.is_authenticated:
        hotel_form = Hotel_Form.objects.get(customer=request.user)
        hotels = Hotel.objects.filter(registation_form = hotel_form)
        return render(request, 'hotel_register/dashboard.html', {"hotels" : hotels})
    
    messages.error(request, "Login required")
    return redirect('login')
    
def owner_hotels(request):
    hotel_form = Hotel_Form.objects.get(customer = request.user)
    hotels = Hotel.objects.filter(registation_form = hotel_form)
    return render(request, 'hotel_register/owner_hotel.html', {"hotels": hotels})

def owner_orders(request):
    hotel_form = Hotel_Form.objects.get(customer = request.user)
    hotels = Hotel.objects.filter(registation_form = hotel_form)
    all_orders = Order.objects.all().order_by('-id')
    
    order_products = []
    for order in all_orders:
        for menu in order.menu_items.all():
            if menu.hotel in hotels:
                order_products.append(order)
                break
    
    
    return render(request, 'hotel_register/owner_order.html', {"order_products": order_products})

def owner_menu_items(request):
    hotel_form = Hotel_Form.objects.get(customer = request.user)
    hotels = Hotel.objects.filter(registation_form = hotel_form)

    menu_items = []
    for hotel in hotels:
        menu_item_set = Menu.objects.filter(hotel = hotel)
        for menu_item in menu_item_set:
            menu_items.append(menu_item)

    return render(request, 'hotel_register/owner_menu.html', {"hotels": menu_items})

def hotel_feedback(request):
    hotel_form = Hotel_Form.objects.get(customer = request.user)
    hotels = Hotel.objects.filter(registation_form = hotel_form)

    feedback = []
    for hotel in hotels:
        reviews = Rating.objects.filter(hotel = hotel)
        for review in reviews:
            feedback.append(review)

    return render(request, 'hotel_register/hotel_rating.html', {"hotel_ratings" : feedback})
