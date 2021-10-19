from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from delivery_boy.models import Delivery, Delivery_Form
from hotel_register.models import Hotel_Form, Hotel, Hotel_Image, Menu
from .models import Application_Form, Cart, Order, Rating, Payment
from django.contrib import messages
from django.db.models import Q
from online_tiffin_service.settings import *
from time import time
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.

import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def home(request):
    if request.user.is_authenticated:
        hotels = Hotel.objects.all().order_by("?")[:7]
        reviews = Rating.objects.all().order_by("?")[:5]
        return render(request, 'food/home.html', {"hotels": hotels, "reviews": reviews})

    else:
        return redirect('login')


def about(request):
    return render(request, 'food/about.html')


def join_us(request):
    try:
        delivery_boy = Delivery.objects.get(customer=request.user)
        return redirect('delivery_boy_dashboard')

    except:
        try:
            delivery_application = Delivery_Form.objects.get(
                customer=request.user)
            return redirect('add_delivery_boy')

        except:
            pass

    try:
        hotel_application = Hotel_Form.objects.get(customer=request.user)

        try:
            hotel = Hotel.objects.filter(registation_form=hotel_application)
            if len(hotel):
                return redirect("dashboard")
            return redirect("add_hotel")

        except:
            return redirect("add_hotel")

    except:
        reviews = Rating.objects.all().order_by("?")[:5]
        return render(request, 'food/landing_page.html', {'reviews': reviews})


def hotel_detail(request, hotel_id, extra=None):
    hotel = Hotel.objects.get(id=hotel_id)
    hotel_extra_images = Hotel_Image.objects.filter(hotel=hotel).order_by("?")
    menu_items = Menu.objects.filter(hotel=hotel)
    hotel_ratings = Rating.objects.filter(hotel=hotel)

    try:
        rating_verify = Rating.objects.get(user=request.user, hotel=hotel)
    except:
        rating_verify = False

    if request.method == "POST":
        try:
            menu_value = request.POST['menu']
            if menu_value:
                menu = Menu.objects.get(id=menu_value)
                try:
                    cart = Cart.objects.get(menu=menu, user=request.user)
                except:
                    cart = False

                if cart:
                    cart.quantity += 1
                    cart.save()
                    messages.success(request, "Cart updated successfully.")
                else:
                    Cart(user=request.user, hotel=hotel,
                         menu=menu, quantity=1).save()
                    messages.success(request, "Item added successfully.")

            else:
                messages.info(request, "Something wen't wrong.")

        except:
            try:
                rating = request.POST['rating']
                review = request.POST['review']
                Rating(user=request.user, hotel=hotel, rating=rating,
                       review=review, is_verified=False).save()
                messages.success(request, "Thanks for rating.")

            except:
                pass

    return render(request, 'food/hotel_detail.html', {"hotel": hotel, "extra": extra, "menu_items": menu_items, "hotel_extra_images": hotel_extra_images, "rating_verify": rating_verify, "hotel_ratings": hotel_ratings})


def my_cart(request):
    carts = Cart.objects.filter(user=request.user)
    total_amount = 0
    user = None
    user = request.user
    for cart in carts:
        total_amount += (cart.menu.price * cart.quantity)

    if request.method == "POST":
        menu_value = request.POST['menu']
        menu = Menu.objects.get(id=menu_value)
        cart = Cart.objects.filter(Q(user=request.user) & Q(menu=menu))
        cart.delete()
        carts = Cart.objects.filter(user=request.user)
        messages.error(request, "Item remove from cart.")

    action = request.GET.get('action')
    order = None
    payment = None
    if action == 'create_payment':
        delivery_time = request.GET['time_delivery']
        time_from = request.GET['time_from']
        print(time_from)
        time_to = request.GET['time_to']
        if not delivery_time:
            messages.error(request, "Delivery time is required.")
            return render(request, 'food/cart.html', {"carts": carts, "total_amount": total_amount, "order": order, "payment": payment})

        order_id = Order()
        order_id.user = request.user
        if time_from and time_to:
            order_id.order_from = time_from
            order_id.order_till = time_to
        order_id.delivery_time = delivery_time
        # order_id.price = price
        order_id.save()

        if order_id.order_from and order_id.order_till:
            format_str = '%Y-%m-%d'
            d1 = datetime.datetime.strptime(order_id.order_from, format_str)
            d2 = datetime.datetime.strptime(order_id.order_till, format_str)
            delta = d2 - d1
            price = (delta.days+1) * total_amount
        else:
            price = total_amount

        order_id.price = price
        order_id.save()

        menu_items = []
        menu_quantity = []
        for menu in carts:
            menu_items.append(menu.menu)
            my_dic = {
                "name": menu.menu.name,
                "quantity": menu.quantity
            }
            menu_quantity.append(my_dic)

        order_id.quantity = menu_quantity
        order_id.menu_items.add(*menu_items)
        order_id.save()

        # for i in order_id.menu_items.all():
        #     print(i)
        # print(ordd.menu_items.all())

        # try:
        #     time_from = request.GET['time_from']
        #     time_to = request.GET['time_to']
        #     time_delivery = request.GET['time_delivery']
        # except:
        #     time_from = None
        #     time_to = None
        # print(time_from, time_to)
        # order_id.order_from =

        amount = int(price*100)
        currency = "INR"
        notes = {
            "email": user.email,
            "name": f'{user.name}'
        }
        receipt = f"onlinetiffinservices-{int(time())}"
        order = client.order.create({
            'receipt': receipt, 'notes': notes, 'amount': amount, 'currency': currency})

        payment = Payment()
        payment.user = request.user
        payment.order_id = order.get('id')
        payment.menu_details = order_id
        payment.save()

    return render(request, 'food/cart.html', {"carts": carts, "total_amount": total_amount, "order": order, "payment": payment})


def plus_cart(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            menu_id = request.GET['menu_id']
            menu = Menu.objects.get(id=menu_id)
            cart = Cart.objects.get(Q(user=request.user) & Q(menu=menu))
            cart.quantity += 1
            cart.save()
            total_amount = 0.0
            item_price = cart.quantity * cart.menu.price
            cart_products = Cart.objects.filter(user=request.user)
            if cart_products:
                for cart_prouct in cart_products:
                    total_amount += (cart_prouct.quantity *
                                     cart_prouct.menu.price)

                data = {
                    'quantity': cart.quantity,
                    'total_amount': total_amount,
                    'item_price': item_price
                }
                return JsonResponse(data)
        else:
            messages.info(request, 'You are not login')
            return redirect('login')

        return render(request, 'food/cart.html', {"carts": cart_products, "total_amount": total_amount})
    # menu_id = request.GET['menu_id']
    # print(menu_id)
    # return JsonResponse("data")


def minus_cart(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            menu_id = request.GET['menu_id']
            menu = Menu.objects.get(id=menu_id)
            cart = Cart.objects.get(Q(user=request.user) & Q(menu=menu))
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()

            total_amount = 0.0
            item_price = cart.quantity * cart.menu.price
            cart_products = Cart.objects.filter(user=request.user)
            if cart_products:
                for cart_prouct in cart_products:
                    total_amount += (cart_prouct.quantity *
                                     cart_prouct.menu.price)

                data = {
                    'quantity': cart.quantity,
                    'total_amount': total_amount,
                    'item_price': item_price
                }
                return JsonResponse(data)
        else:
            messages.info(request, 'You are not login')
            return redirect('login')

        return render(request, 'food/cart.html', {"carts": cart_products, "total_amount": total_amount})
    # menu_id = request.GET['menu_id']
    # print(menu_id)
    # return JsonResponse("data")


@csrf_exempt
def verifyPayment(request):
    if request.method == 'POST':
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = str(razorpay_payment_id)
            payment.status = True
            payment.save()

            print("Hello World")
            print(request.user)
            try:
                carts = Cart.objects.filter(user=request.user)
                print(carts)
                for cart in carts:
                    cart.delete()
            except:
                pass

            return redirect('home')
        except:
            return redirect('home')


def orders(request):
    if request.user.is_authenticated:
        customer_orders = Order.objects.filter(user=request.user).order_by("-id")

        for customer_order in customer_orders:
            print(customer_order.order_from)

        return render(request, 'food/order.html', {"order_products": customer_orders})

    return redirect('login')


def search_items(request):
    search_query = request.GET['search']
    menu_items = Menu.objects.filter(
        Q(name__icontains=search_query) | Q(description__icontains=search_query))
    print(menu_items)
    hotels = Hotel.objects.filter(Q(name__icontains=search_query) | Q(
        city__icontains=search_query) | Q(address__icontains=search_query))
    print(hotels)

    return render(request, 'food/search.html', {"menu_items": menu_items, "hotels": hotels})


def all_hotel(request):
    hotels = Hotel.objects.all()
    return render(request, 'food/all_hotel.html', {"hotels": hotels, "menu": False})


def all_menu(request):
    menus = Menu.objects.all()
    return render(request, 'food/all_hotel.html', {"hotels": menus, "menu": True})
