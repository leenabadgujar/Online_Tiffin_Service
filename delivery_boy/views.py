from food.models import Application_Form, Order
from hotel_register.models import Hotel_Form
from django.contrib import messages
from delivery_boy.models import Delivery, Delivery_Form, Delivery_payment
from django.shortcuts import redirect, render
from online_tiffin_service.settings import *
from time import time
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.http.response import HttpResponse, JsonResponse
# Create your views here.

import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def delivery_boy_form(request):
    if request.user:
        if request.method == "POST":
            date_of_birth = request.POST['date']
            gender = request.POST['gender']
            city = request.POST['city']
            address = request.POST['address']
            code = request.POST['code']
            experience = request.POST['experience']
            licenses = request.POST['license']
            working_form = request.POST['from']
            working_to = request.POST['to']
            weekend = request.POST['work']
            money = request.POST['money']
            range_of_delivery = request.POST['range']
            vehicle = request.POST['vehicle']

            Delivery_Form(customer=request.user, date_of_birth=date_of_birth, gender=gender, city=city, address=address, pincode=code, experience=experience, licenses=licenses,
                          working_form=working_form, working_to=working_to, weekends=weekend, money=money, range_of_delivery=range_of_delivery, vehicle=vehicle).save()
            messages.success(request, "Form submitted successfully.")
            return redirect('home')

        try:
            hotel_form = Hotel_Form.objects.get(customer=request.user)
            if hotel_form.status == "Rejected":
                return render(request, 'delivery_boy/delivery_boy.html')

            elif hotel_form.status == "Pending":
                messages.info(
                    request, 'Your application for hotel owner is pending.')
                return redirect('home')

            else:
                return redirect('add_hotel')

        except:
            try:
                delivery_form = Delivery_Form.objects.get(
                    customer=request.user)
                if delivery_form.status == "Rejected":
                    messages.error(request, 'Your application is rejected.')
                    return redirect('home')
                    # return render(request, 'delivery_boy/delivery_boy.html')

                elif delivery_form.status == "Pending":
                    messages.error(request, 'Your application is pending.')
                    return redirect('home')

                else:
                    messages.error(request, 'Your application is accepted.')
                    return redirect('home')

            except:
                return render(request, 'delivery_boy/delivery_boy.html')

    return redirect('login')


def add_information(request):
    if request.user.is_authenticated:
        try:
            delivery_form = Delivery_Form.objects.get(customer=request.user)
        except:
            delivery_form = False

        if request.method == "POST":
            try:
                wroking_from = request.POST['from']
                till = request.POST['till']
                cost = request.POST['cost']
                delivery_range = request.POST['range']
                vehicle = request.POST['vehicle']
                picture = request.FILES['picture']
                aadhar_card = request.FILES['aadhar_card']
                driving_licence = request.FILES['driving_licence']

                Delivery(customer=request.user, date_of_birth=delivery_form.date_of_birth, gender=delivery_form.gender, city=delivery_form.city, address=delivery_form.address, pincode=delivery_form.pincode,
                         working_form=wroking_from, working_to=till, money=cost, range_of_delivery=delivery_range, vehicle=vehicle, image=picture, aadhar_card_image=aadhar_card, driving_licence_image=driving_licence).save()
                messages.success(request, "Form submitted successfully.")
                return redirect("home")

            except:
                messages.error(request, "All fields required.")
                return render(request, 'delivery_boy/add_delivery.html', {"delivery_form": delivery_form})

        if delivery_form:
            try:
                verify = Delivery.objects.get(customer=request.user)
            except:
                verify = False

            if verify:
                messages.error(request, "You already register in our site.")
                return redirect('home')

            else:
                if delivery_form.status == "Pending":
                    messages.error(
                        request, "Application for delivery boy is pending.")
                    return redirect('home')

                if delivery_form.status == "Rejected":
                    messages.error(
                        request, "Application for delivery boy is rejected.")
                    return redirect('home')
                else:
                    return render(request, 'delivery_boy/add_delivery.html', {"delivery_form": delivery_form})

        else:
            messages.error(request, "You need to apply for delivery boy.")
            return redirect('home')

    return redirect('login')


def delivery_boy_dashboard(request):
    if request.user.is_authenticated:
        delivery_boy = Delivery.objects.get(customer=request.user)

        applications = Application_Form.objects.filter(
            delivery_boy=delivery_boy)
        accepted_applications = Application_Form.objects.filter(
            delivery_boy=delivery_boy, status="Accepted")[:3]

        pending = 0
        accepted = 0
        rejected = 0
        order = 0
        for application in applications:
            if application.status == "Pending":
                pending += 1
            elif application.status == "Accepted":
                accepted += 1
            else:
                rejected += 1
            order += 1

        return render(request, 'delivery_boy/delivery_dashboard.html', {"applications": applications, "pending": pending, "accepted": accepted, "rejected": rejected, "order": order, "accepted_applications": accepted_applications})

    else:
        return redirect('login')


def pending(request):
    if request.method == "POST":
        input_value = request.POST['application']
        application_id = request.POST['application_id']
        application = Application_Form.objects.get(id=application_id)
        if input_value:
            if input_value == "Yes":
                application.status = "Accepted"
                application.save()
                messages.success(request, "Application accepted.")
            else:
                application.status = "Rejected"
                application.save()
                messages.success(request, "Application rejected.")

    delivery_boy = Delivery.objects.get(customer=request.user)
    applications = Application_Form.objects.filter(
        delivery_boy=delivery_boy, status="Pending")
    return render(request, 'delivery_boy/pending.html', {"applications": applications})


def rejected(request):
    delivery_boy = Delivery.objects.get(customer=request.user)
    applications = Application_Form.objects.filter(
        delivery_boy=delivery_boy, status="Rejected")
    reject = applications
    return render(request, 'delivery_boy/accepted.html', {"applications": applications, "reject": True})


def accepted(request):
    delivery_boy = Delivery.objects.get(customer=request.user)
    applications = Application_Form.objects.filter(
        delivery_boy=delivery_boy, status="Accepted")
    reject = applications
    return render(request, 'delivery_boy/accepted.html', {"applications": applications, "reject": False})


def book_delivery_boy(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            delivery_boy_id = request.POST['delivery_boy']
            delivery_time = request.POST['delivery_time']
            delivery_start = request.POST['start']
            delivery_end = request.POST['end']
            pick_up_address = request.POST['pick_up_address']
            delivery_address = request.POST['delivery_address']

            if delivery_boy_id and delivery_time:
                delivery_boy = Delivery.objects.get(id=delivery_boy_id)
                Application_Form(user=request.user, delivery_start=delivery_start, delivery_boy=delivery_boy, delivery_time=delivery_time, delivery_end=delivery_end, pickup_address=pick_up_address, delivery_address=delivery_address).save()
                messages.success(request, "Apply successfully.")
                return redirect('home')
            else:
                messages.error(request, "Try again")

        application_forms = Application_Form.objects.filter(user=request.user)
        delivery_boys = Delivery.objects.filter(city__iexact=request.user.city)

        applications = None
        total_amount = 0
        application_form = application_forms.last()
        
        if application_form.status == "Accepted":
            d1 = application_form.delivery_start
            d2 = application_form.delivery_end
            delta = d2 - d1
            total_amount = (delta.days+1) * \
                application_form.delivery_boy.money
            applications = application_form
            delivery_boys = None

        action = request.GET.get('action')
        order = None
        if action == 'create_payment':
            amount = int(total_amount*100)
            currency = "INR"
            notes = {
                "email": request.user.email,
                "name": f'{request.user.name}'
            }
            receipt = f"onlinetiffinservices-{int(time())}"
            order = client.order.create(
                {'receipt': receipt, 'notes': notes, 'amount': amount, 'currency': currency})

            application_forms = Application_Form.objects.filter(
                user=request.user)
            valid_applications = []
            for applications in application_forms:
                if applications.status == "Accepted":
                    valid_applications.append(applications)

            payment = Delivery_payment()
            payment.user = request.user
            payment.order_id = order.get('id')
            payment.application_Form = valid_applications[-1]
            payment.save()

        
        show = False

        try:
            delivery_boy_payment = Delivery_payment.objects.get(application_Form = applications)
        except:
            delivery_boy_payment = False

        print(delivery_boy_payment)
        if not delivery_boy_payment:
            show = True
            return render(request, 'food/book_delivery_boy.html', {"delivery_boys": delivery_boys, "applications": applications, "total_amount": total_amount, "order": order, "show" : show})
        else:
            if date.today() >= applications.delivery_end:
                delivery_boys = Delivery.objects.filter(city__iexact=request.user.city)
            else:
                show = False
            return render(request, 'food/book_delivery_boy.html', {"delivery_boys": delivery_boys, "applications": applications, "total_amount": total_amount, "order": order, "show" : show})

    else:
        return redirect('login')


@csrf_exempt
def verifyPayment(request):
    if request.method == 'POST':
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            payment = Delivery_payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = str(razorpay_payment_id)
            payment.status = True
            payment.save()
            messages.success(request, "Payment successful.")
            return redirect('home')
        except:
            return HttpResponse("Invalid Payment Details")
