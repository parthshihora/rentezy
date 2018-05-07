from django.conf import settings
from django.core.mail import send_mail

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import CarForm, ResForm, FilterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
from datetime import datetime
import threading
#import datetime
# from django.contrib.gis.geoip2 import GeoIP2

def OwnerDocs(request,object_id):
    owner = Reg_Owner.objects.get(pk=object_id)
    return render(request, "team6/ownerdoc.html", {'owner': owner})


def getlocation(request):
    threading.Timer(120,getlocation,[request]).start()
    print datetime.utcnow()
    g = GeoIP2()
    #ip = request.META.get('REMOTE_ADDR', None)
    ip = '134.201.250.155'
    #print("******meta*******",request.META['REMOTE_ADDR'])
    if (not ip or ip == '127.0.0.1') and request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    elif ip:
        city = g.city(ip)['city']
        latitude = g.city(ip)['latitude']
        longitude = g.city(ip)['longitude']
        location = [latitude,longitude,city]
    else:
        city = "Albany"# set default city
    return location


'''def pasttrips(request):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    today = datetime.today().strftime('%Y-%m-%d')'''

def mytrips(request):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    today = datetime.today().strftime('%Y-%m-%d')
    #reservations = Reservation.objects.filter(user=request.session['id'])
    #date = reservations.drop_date
    #reservations = Reservation.objects.filter(user=request.session['id'])
    #ddate = reservation.drop_date
    #print("**********",date)

    #reservations = Reservation.objects.filter(user=request.session['id'],drop_date__range=['2018-04-23',today])
    if request.session['role'] == 'customer':
        reservations = Reservation.objects.filter(customer=request.session['id'],drop_date__lte=today)
    elif request.session['role'] == 'owner':
        reservations = Reservation.objects.filter(owner=request.session['id'], drop_date__lte=today)

    return render(request, "mytrips.html", {'reservations': reservations})

@csrf_exempt
def allCars(request):
    if 'id' not in request.session:
        return redirect('/errorpage/')

    form = FilterForm()
    cars = Car.objects.exclude(Reserved="Yes")
    if request.method == "POST":
        car_type=request.POST['cartype']
        no_of_pass=request.POST['nop']
        sorting = request.POST['sortby']
        print car_type + no_of_pass
        if car_type=='none' and no_of_pass == "10" and sorting=="lowtohigh":
            cars = Car.objects.exclude(Reserved="Yes").order_by('priceperhour')
    
        elif car_type=='none' and no_of_pass == "10" and sorting=="hightolow":
            cars = Car.objects.exclude(Reserved="Yes").order_by('-priceperhour')
    

        elif car_type != 'none' and no_of_pass == "10" and sorting=="lowtohigh":
            cars = Car.objects.exclude(Reserved="Yes").filter(cartype__contains=car_type).order_by("priceperhour")

        elif car_type != 'none' and no_of_pass == "10" and sorting=="hightolow":
            cars = Car.objects.exclude(Reserved="Yes").filter(cartype__contains=car_type).order_by("-priceperhour")

        elif car_type == 'none' and no_of_pass != "10" and sorting=="lowtohigh":
            cars = Car.objects.exclude(Reserved="Yes").filter(passengerCapacity__exact=no_of_pass).order_by("priceperhour")

        elif car_type == 'none' and no_of_pass != "10" and sorting=="hightolow":
            cars = Car.objects.exclude(Reserved="Yes").filter(passengerCapacity__exact=no_of_pass).order_by("-priceperhour")
            
        else:
            cars = Car.objects.exclude(Reserved="Yes").filter(cartype__contains=car_type, passengerCapacity__exact=no_of_pass)
            

    return render(request, "team6/allcars.html", {'form': form, 'cars': cars})

def notifications(request):
    if 'id' not in request.session:
        return redirect('/errorpage/')
   # reservation = Reservation.objects.filter(owner=request.session['id'])
    today = datetime.today().strftime('%Y-%m-%d')
    reservation = Reservation.objects.filter(owner=request.session['id'],drop_date__gte=today)
    return render(request, "Notifications.html", {'reservation': reservation})


def filteredcars(request):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    city=request.GET.get('name')
    cars = Car.objects.filter(pickuplocation__contains=city,Reserved="No")
    #cars = cars.objects.exclude(Reserved="Yes")
    if request.method == "POST":
        car_type=request.POST['cartype']
        no_of_pass=request.POST['nop']
        print car_type + no_of_pass
        if car_type=='none' and no_of_pass == 10:
            cars = Car.objects.exclude(Reserved="Yes")
        elif car_type != 'none' and no_of_pass == 10:
            cars = Car.objects.exclude(Reserved="Yes").filter(cartype__contains=car_type)
        elif car_type == 'none' and no_of_pass != 10:
            cars = Car.objects.exclude(Reserved="Yes").filter(user__car__passengerCapacity__exact=no_of_pass)
        else:
            cars = Car.objects.exclude(Reserved="Yes").filter(cartype__contains=car_type, user__car__passengerCapacity__exact=no_of_pass)

    return render(request, "team6/filteredcars.html", {'cars': cars})


def objectDelete(request, object_id):
    print("*****", object_id)
    object = get_object_or_404(Car, pk=object_id)
    object.delete()
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect('/yourcars/')

def approvedOwners(request,object_id):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    owner = Reg_Owner.objects.get(pk=object_id)
    print("*******",owner)
    owner.status = "Approved"
    owner.save()
    return HttpResponseRedirect('/allowners/')

def rejectOwners(request,object_id):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    owner = Reg_Owner.objects.get(pk=object_id)
    print("*******",owner)
    owner.status = "Rejected"
    owner.save()
    return HttpResponseRedirect('/allowners/')    

def modifyCar(request, object_id):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    # object = get_object_or_404(Car, pk=object_id)
    if request.POST:
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = Car.objects.get(pk=object_id)
            car.car_pic = request.FILES.get("car_pic")
            form = CarForm(request.POST, instance=car)
            form.save()
            return HttpResponseRedirect('/yourcars/')
    else:
        car = Car.objects.get(pk=object_id)
        form = CarForm(instance=car)
    return render(request, "carform.html", {'form': form})


def owner_profile(request):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    return render(request, "ownerprofile.html")


def add_car(request):  # carentry car instead of this
    if 'id' not in request.session:
        return redirect('/errorpage/')
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES);
        if form.is_valid():
            cars = form.save(commit=False)
            cars.owner = Reg_Owner.objects.get(pk=request.session['id'])
            cars.car_pic = request.FILES.get("car_pic")
            cars.save()
            # form.save()
            return redirect('/yourcars/')
    else:
        form = CarForm()
    return render(request, "carform.html", {'form': form})


def start_page(request):
    return render(request, "startpage.html")


def your_cars(request):  # CarView class instead of this
    if 'id' not in request.session:
        return redirect('/errorpage/')
    # user = Car.user
    cars = Car.objects.filter(owner=request.session['id'])
    return render(request, "team6/owner_cars.html", {'cars': cars})


def ownersignup(request):
        errors = []
        if request.method == 'POST':
            form = OwnerSignUpForm(request.POST,request.FILES)
            if form.is_valid():
                userdata = form.save(commit=False)
                cleaned_username = form.cleaned_data.get('username').lower()
                cleaned_password = form.cleaned_data.get('password')
                role = 'owner'
                regs_count = Reg_Owner.objects.filter(username=cleaned_username).count()
                if regs_count >= 1:
                    errors.append('User Name already exists');
                else:
                    userdata.__setattr__('username',cleaned_username)
                    userdata.__setattr__('password',cleaned_password)
                    if role == "owner":
                        userdata.__setattr__('status',"Not Approved")
                    else:
                        userdata.__setattr__('status',"Approved")
                    userdata.license = request.FILES.get("license")  
                    form.save()
                    messages.success(request, 'Registration Successful')
        else:
            form = OwnerSignUpForm()
        return render(request, 'ownersignup.html', {'form': form, 'error_msg': errors})


def customersignup(request):
    errors = []
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            userdata = form.save(commit=False)
            cleaned_username = form.cleaned_data.get('username').lower()
            cleaned_password = form.cleaned_data.get('password')
            role = 'owner'
            regs_count = Reg_Customer.objects.filter(username=cleaned_username).count()
            if regs_count >= 1:
                errors.append('User Name already exists');
            else:
                userdata.__setattr__('username', cleaned_username)
                userdata.__setattr__('password', cleaned_password)
                if (role == "owner"):
                    userdata.__setattr__('status', "Not Approved")
                else:
                    userdata.__setattr__('status', "Approved")
                form.save()
                messages.success(request, 'Registration Successful')
    else:
        form = CustomerSignUpForm()
    return render(request, 'customersignup.html', {'form': form, 'error_msg': errors})


def ownerloginform(request):
    if request.method == "POST":
        form = OwnerLoginForm(request.POST)
        # loc=getlocation(request)
        # print form.data['username']
        if form.is_valid():
            usrname = form.cleaned_data['username'].lower()
            try:
                regs = Reg_Owner.objects.get(username=usrname)
                print regs
                # regs = Reg_Owner.objects.get(username=usrname)
                # status = form.cleaned_data['status']
                if regs.username == usrname and regs.password == form.cleaned_data['password']:
                    request.session['id'] = regs.id
                    request.session['username'] = form.cleaned_data['username']
                    request.session['password'] = form.cleaned_data['password']
                    request.session['role'] = 'owner'
                    regs.role = 'owner'
                else:
                    messages.warning(request, 'Enter a valid username and password combination')
                if regs.status == "Approved":
                    return redirect('/yourcars/')
                elif regs.status == "Not Approved":
                    messages.warning(request, 'You are not  yet Approved')
                elif regs.status == "Rejected":
                    messages.warning(request, 'You are rejected, please contact admin')
            except Exception as e:
                    messages.warning(request, 'Enter a valid username and password combination')
    else:
        form = OwnerLoginForm()
    return render(request, 'ownerlogin.html', {'form': form})


def customerloginform(request):
    if request.method == "POST":
        form = CustomerLoginForm(request.POST)
        loc=getlocation(request)
        # print form.data['username']
        if form.is_valid():
            usrname = form.cleaned_data['username'].lower()
            try:
                regs = Reg_Customer.objects.get(username=usrname)
                # status = form.cleaned_data['status']
                if regs.username == usrname and regs.password == form.cleaned_data['password']:
                    request.session['id'] = regs.id
                    request.session['username'] = form.cleaned_data['username']
                    request.session['password'] = form.cleaned_data['password']
                    request.session['role'] = 'customer'
                    regs.role = 'customer'
                    print "inside first IF"
                    print regs.role
                    print loc

                if (regs.role == "customer"):
                    print loc[0]
                    print loc
                    regs.latitude = loc[0]
                    regs.longitude = loc[1]
                    regs.location = loc[2]
                    regs.save()
                    return redirect('/allcars/')
            except Exception as e:
                messages.warning(request, 'Enter a valid username and password combination')
    else:
        form = CustomerLoginForm()
    return render(request, 'customerlogin.html', {'form': form})


def adminloginform(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        # loc=getlocation(request)
        # print form.data['username']
        if form.is_valid():
            usrname = form.cleaned_data['username'].lower()
            regs = Reg_Admin.objects.get(username=usrname)
            # status = form.cleaned_data['status']
            if regs.username == usrname and regs.password == form.cleaned_data['password']:
                request.session['id'] = regs.id
                request.session['username'] = form.cleaned_data['username']
                request.session['password'] = form.cleaned_data['password']
                request.session['role'] = 'admin'
                regs.role = 'admin'
            return redirect('/allowners/')
    else:
        form = AdminLoginForm()
    return render(request, 'adminlogin.html', {'form': form})


def logout_view(request):
    try:
        del request.session['id']
        del request.session['role']
        del request.session['username']
        del request.session['password']

    except KeyError:
        pass
    return redirect('/startpage/')


def delete_reservation(request, object_id):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    car = Car.objects.get(pk=object_id)
    reservation = Reservation.objects.get(carid=object_id)
    car.Reserved = "No"
    reservation.status = "Deleted"
    car.save()
    reservation.save()
    #object = get_object_or_404(Reservation, carid=object_id)
    #object.delete()
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect('/myreservations/')


def modify_reservation(request,object_id):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    #reservation = Reservation.objects.get(pk=object_id)
    car = Car.objects.get(pk=object_id)
    #print("************",car)
    if request.method == 'POST':
        form = ResForm(request.POST)
        if form.is_valid():
            reservation = Reservation.objects.get(carid=object_id)
            reservation.status = "Modified"

            pickup_date = form.cleaned_data['pickup_date']
            drop_date1 = form.cleaned_data['drop_date']
            if(pickup_date>drop_date1):
                messages.info(request,object_id, 'Please enter correct dates')
            else:
                drop_date2 = str(form.cleaned_data['drop_date'])
                drop_date = datetime.strptime(drop_date2, "%Y-%m-%d")
                reservation.drop_date = drop_date
               # car.save()
                form = ResForm(request.POST,instance=reservation)
                form.save()
                reservation.save()
                subject = "Notifications from Rentezy, Reservation of your car has been Modified"
                message1 = "Reservation of your car "+ car.modelName +" hase been modified by " + reservation.customer.first_name + " "+ reservation.customer.first_name
                message2 = "\nYou can contact your customer on " + reservation.customer.email
                message3 = "\nReservation Details\n"
                message4 = "Pickup Date:"+str(reservation.pickup_date) + "\n" + "Drop Date:"+str(reservation.drop_date) 
                message = message1 + message2 + message3 + message4
                reservation.save()
                from_email = settings.EMAIL_HOST_USER
                to_email = car.owner.email
                to_list = [to_email]
                send_mail(subject,message,from_email,to_list,fail_silently=True)
                return HttpResponseRedirect('/myreservations/')
    else:
        #reservation = Reservation.objects.get(pk=object_id)
        form = ResForm()
    return render(request,"team6/resform.html",{'form':form,'car':car})


def make_reservation(request, object_id):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    car = Car.objects.get(pk=object_id)
    
    if(Reservation.objects.filter(carid=object_id).exists()):
        reservation = Reservation.objects.get(carid=object_id)
        if(reservation.status=="Deleted"):
            object = get_object_or_404(Reservation, carid=object_id)
            object.delete()

    # owner = UserData.objects.get(pk=car.user)
    if request.method == 'POST':
        form = ResForm(request.POST)
        if form.is_valid():
            # reservations=form.save(commit=False)
            car = Car.objects.get(pk=object_id)
            #owner = UserData.objects.get(pk=car.user)
            reservation = form.save(commit=False)
            #car.user = Reg.objects.get(pk=request.session['id'])
            reservation.customer = Reg_Customer.objects.get(pk=request.session['id'])
            reservation.carid_id = car.id
            car.Reserved = "Yes"
            # reservation.owner = car.user.username
            reservation.owner = Reg_Owner.objects.get(pk=car.owner_id)

            pickup_date = form.cleaned_data['pickup_date']
            drop_date1 = form.cleaned_data['drop_date']
            if(pickup_date>drop_date1):
                messages.info(request,object_id, 'Please enter correct dates')
            else:
                drop_date2 = str(form.cleaned_data['drop_date'])
                drop_date = datetime.strptime(drop_date2, "%Y-%m-%d")
                reservation.drop_date = drop_date
                car.save()
                reservation.save()
                subject = "Notifications from Rentezy, Your car has been reserved"
                message1 = "Your car "+ car.modelName + " haowse been reserved by " + reservation.customer.first_name + " "+ reservation.customer.last_name
                message2 = "\nYou can contact your customer on " + reservation.customer.email
                message3 = "\nReservation Details\n"
                message4 = "Pickup Date:"+str(reservation.pickup_date) + "\n" + "Drop Date:"+str(reservation.drop_date) 
                message = message1 + message2 + message3 + message4

                from_email = settings.EMAIL_HOST_USER
                to_email = car.owner.email
                to_list = [to_email]

                c_subject = "Thank you for renting car with Rentezy" # Mail to customer
                c_m1 = "You have reserved  "+ car.modelName
                c_m2 = "\nOwner of you car is "+ reservation.owner.first_name + " " + reservation.owner.last_name
                c_m3 = "\nReservation Details\n"
                c_m4 = "Pickup Date:"+str(reservation.pickup_date) + "\n" + "Drop Date:"+str(reservation.drop_date) + "\nPickup location:" + car.pickuplocation
                c_m = c_m1 + c_m2 + c_m3 + c_m4
                c_email  = reservation.customer.email
                c_to_list = [c_email]

                send_mail(subject,c_m,from_email,c_to_list,fail_silently=True) # Mail to customer
                send_mail(subject,message,from_email,to_list,fail_silently=True)
                return redirect('/myreservations/')

    else:
        form = ResForm()
        car.Reserved = "Reserved"
    return render(request, "team6/resform.html", {'form': form,'car':car})

def my_reservations(request):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    #Car.objects.filter(user=request.session['id'])
    today = datetime.today().strftime('%Y-%m-%d')
    reservations = Reservation.objects.filter(customer=request.session['id'],drop_date__gte=today)
    # cars = []
    # for reservation in reservations:
    #     cars.append(Car.objects.get(pk=reservation.carid))
    return render(request, "team6/myreservations.html", {'reservations': reservations})

def test_session(request):
    request.session.set_test_cookie()
    return HttpResponse("Testing session cookie")


def test_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("Cookie test passed")
    else:
        response = HttpResponse("Cookie test failed")
    return response

def allOwners(request):
    owners = Reg_Owner.objects.all()
    return render(request, "AllOwner.html", {'owners': owners})


def adduserfeedback(request, object_id):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    if request.method == "POST":
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            # True == Customer to owner feedback
            # False == Owner to Customer feedback
            if request.session['role'] == 'owner':
                user = Reg_Customer.objects.get(pk=object_id)
                print("in owner feedbacks***")
                feedbacks = Feedback.objects.filter(owner_id=request.session['id'],customer_id=user.id,direction=False)
                if(feedbacks):
                    messages.info(request,object_id, 'You have already give feedback to this customer')
                else:
                    feedback.__setattr__('owner', Reg_Owner.objects.get(pk=request.session['id']))
                    feedback.__setattr__('time', timezone.now())
                    feedback.__setattr__('direction', False)
                    user.sum_rating = user.sum_rating + int(form.data['rating'])
                    user.num_feedbacks = int(user.num_feedbacks)+1
                    feedback.__setattr__('customer', user)
                    user.save()
                    feedback.save()
                    return redirect('/myfeedbacks/')
            elif request.session['role'] == 'customer':
                user = Reg_Owner.objects.get(pk=object_id)
                feedbacks = Feedback.objects.filter(customer_id=request.session['id'],owner_id=user.id,direction=True)
                if(feedbacks):
                    print("feedback is given already*******")
                    messages.info(request,object_id, 'You have already give feedback to this car owner')
                else:
                    feedback.__setattr__('customer', Reg_Customer.objects.get(pk=request.session['id']))
                    feedback.__setattr__('time', timezone.now())
                    feedback.__setattr__('direction', True)
                    user.sum_rating = user.sum_rating + int(form.data['rating'])
                    user.num_feedbacks = int(user.num_feedbacks)+1
                    feedback.__setattr__('owner', user)
                    user.save()
                    feedback.save()
                    return redirect('/myfeedbacks/')
    else:
        form = UserFeedbackForm()
    return render(request, 'addfeedback.html', {'form': form})


def displayfeedbacks(request):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    if request.session['role'] == 'customer':
        feedbacks = Feedback.objects.filter(customer=request.session['id'], direction=False)
    elif request.session['role'] == 'owner':
        print("in owner feedbacks****")
        feedbacks = Feedback.objects.filter(owner=request.session['id'], direction=True)
    #else:
    #    feedbacks = Feedback.objects.all()
    return render(request, "myfeedbacks.html", {'feedbacks': feedbacks})


def errorpage(request):
    return render(request, 'errorpage.html')


def showmap(request, object_id):
    if 'id' not in request.session:
        return redirect('/errorpage/')
    customer = Reg_Customer.objects.get(pk=object_id)
    print customer.latitude, customer.longitude
    # mapdetails = {'url' : 'https://maps.googleapis.com/maps/api/js?key= AIzaSyD2OG1L2BQGatYPDcAKj6hq9uv_sdUlwO4&callback=initMap', 'lat': customer.latitude, 'long':customer.longitude}
    # # url = 'https://www.google.com/maps/embed/v1/place?key= AIzaSyD2OG1L2BQGatYPDcAKj6hq9uv_sdUlwO4 &q='' &center='+customer.latitude+','+customer.longitude+' &zoom=15 &maptype=roadmap'
    # mapdetails['url'] = "https://maps.googleapis.com/maps/api/js?key= AIzaSyD2OG1L2BQGatYPDcAKj6hq9uv_sdUlwO4 &callback=initMap"
    # mapdetails['lat'] = customer.latitude
    # mapdetails['long'] = customer.longitude
    url = "https://maps.googleapis.com/maps/api/js?key=AIzaSyAn3ejrJbVbRHwWgyuKug41VxShwB-PeSw&callback=initMap"
    return render(request, 'showmap.html', {'url': url, 'lat': customer.latitude, 'longitude': customer.longitude})
