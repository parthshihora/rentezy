from django.shortcuts import render
from .forms import CarForm, ResForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.shortcuts import render, redirect
from .models import Car, Reservation, UserData, Reg
from .forms import SignUpForm, LoginForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse






def allCars(request, type='none', no_of_pass=0, sortby='price'):
    if type=='none' and no_of_pass == 0:
        cars = Car.objects.exclude(Reserved="Yes")
    elif type != 'none' and no_of_pass == 0:
        cars = Car.objects.exclude(Reserved="Yes").filter(cartype__contains=type)
    elif type == 'none' and no_of_pass != 0:
        cars = Car.objects.exclude(Reserved="Yes").filter(user__car__passengerCapacity__exact=no_of_pass)
    else:
        cars = Car.objects.exclude(Reserved="Yes").filter(cartype__contains=type, user__car__passengerCapacity__exact=no_of_pass)

    return render(request, "team6/allcars.html", {'cars': cars})

def notifications(request):
    reservation = Reservation.objects.filter(owner=request.session['username'])
    print("**************",request.session['username'])
    print("****************",reservation)
    return render(request, "Notifications.html", {'reservation': reservation})



def filteredcars(request):
    city=request.GET.get('name')
    cars = Car.objects.filter(pickuplocation__contains=city)
    return render(request, "team6/filteredcars.html", {'cars': cars})


def objectDelete(request, object_id):
    print("*****", object_id)
    object = get_object_or_404(Car, pk=object_id)
    object.delete()
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect('/yourcars/')

def approvedOwners(request,object_id):
    owner = Reg.objects.get(pk=object_id)
    print("*******",owner)
    owner.status = "Approved"
    owner.save()
    return HttpResponseRedirect('/allowners/')

def rejectOwners(request,object_id):
    owner = Reg.objects.get(pk=object_id)
    print("*******",owner)
    owner.status = "Rejected"
    owner.save()
    return HttpResponseRedirect('/allowners/')    

def modifyCar(request, object_id):
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
    # form = CarForm()

    # print("****Modify",object.modelNumber)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, "carform.html", {'form': form})


def owner_profile(request):
    return render(request, "ownerprofile.html")


def add_car(request):  # carentry car instead of this
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES);
        if form.is_valid():
            cars = form.save(commit=False)
            #cars.user = request.user
            print("^^^^^^^^^^above form")
            cars.user = Reg.objects.get(pk=request.session['id'])
            print("^^^^^^^^^^below form",cars.user)
            cars.car_pic = request.FILES.get("car_pic")
            print("very below")
            cars.save()
            # form.save()
            return redirect('/yourcars/')
    else:
        form = CarForm()
    return render(request, "carform.html", {'form': form})


def start_page(request):
    return render(request, "startpage.html")


def your_cars(request):  # CarView class instead of this
    # user = Car.user
    cars = Car.objects.filter(user=request.session['id'])
    return render(request, "team6/owner_cars.html", {'cars': cars})


def signup(request):
        errors = []
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                userdata = form.save(commit=False)
                cleaned_username = form.cleaned_data.get('username').lower()
                cleaned_password = form.cleaned_data.get('password')
                role = form.cleaned_data.get('role')
                regs_count = Reg.objects.filter(username=cleaned_username).count()
                if regs_count >= 1:
                    errors.append('User Name already exists');
                else:
                    userdata.__setattr__('username',cleaned_username)
                    userdata.__setattr__('password',cleaned_password)
                    if(role=="owner"):
                        userdata.__setattr__('status',"Not Approved")
                    else:
                        userdata.__setattr__('status',"Approved")
                    form.save()
                    messages.success(request, 'Registration Successful')
        else:
            form = SignUpForm()
        return render(request, 'register.html', {'form': form, 'error_msg': errors})

def loginform(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        # print form.data['username']
        if form.is_valid():
            usrname = form.cleaned_data['username'].lower()
            regs = Reg.objects.get(username=usrname)
            #status = form.cleaned_data['status']
            if regs.username == usrname and regs.password == form.cleaned_data['password'] :
                request.session['id'] = regs.id
                request.session['username'] = form.cleaned_data['username']
                request.session['password'] = form.cleaned_data['password']
        if(form.data['role'] == "customer"):
            return redirect('/allcars/')
        elif(regs.status == "Approved"):
            return redirect('/accounts/profile')
        elif(regs.status == "Not Approved"):
            messages.warning(request, 'You are not  yet Approved')
        elif(regs.status == "Rejected"):
            messages.warning(request, 'You are rejected, please contact admin')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    try:
        del request.session['id']

    except KeyError:
        pass
    #logout(request)

        #return HttpResponseRedirect('/startpage/')

    #return render(request, "team6/form.html", {})
    return redirect('/startpage/')


    #return render(request, "team6/form.html", {})
    return redirect('/startpage/')

def delete_reservation(request, object_id):
    car = Car.objects.get(pk=object_id)
    car.Reserved = "No"
    car.save()
    object = get_object_or_404(Reservation, carid=object_id)
    object.delete()
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect('/myreservations/')


def modify_reservation(request,object_id):
    #reservation = Reservation.objects.get(pk=object_id)
    car = Car.objects.get(pk=object_id)
    #print("************",car)
    if request.method == 'POST':
        form = ResForm(request.POST)
        if form.is_valid():
            reservation = Reservation.objects.get(carid=object_id)
            print("********Reservation",reservation)
            form = ResForm(request.POST,instance=reservation)
            form.save()
            return HttpResponseRedirect('/myreservations/')
    else:
        #reservation = Reservation.objects.get(pk=object_id)
        form = ResForm()
    return render(request,"team6/resform.html",{'form':form,'car':car})


def make_reservation(request, object_id):
    car = Car.objects.get(pk=object_id)
    # owner = UserData.objects.get(pk=car.user)
    if request.method == 'POST':
        form = ResForm(request.POST)
        if form.is_valid():
            # reservations=form.save(commit=False)
            car = Car.objects.get(pk=object_id)
            #owner = UserData.objects.get(pk=car.user)
            reservation = form.save(commit=False)
            #car.user = Reg.objects.get(pk=request.session['id'])
            reservation.user = Reg.objects.get(pk=request.session['id'])
            reservation.carid_id = car.id
            car.Reserved = "Yes"
            reservation.owner = car.user.username
            car.save()
            reservation.save()
            return redirect('/myreservations/')
    else:
        form = ResForm()
        car.Reserved = "Reserved"
    return render(request, "team6/resform.html", {'form': form,'car':car})

def my_reservations(request):
    #Car.objects.filter(user=request.session['id'])
    reservations = Reservation.objects.filter(user=request.session['id'])
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
    owners = Reg.objects.filter(role='owner')
    return render(request, "AllOwner.html", {'owners': owners})

