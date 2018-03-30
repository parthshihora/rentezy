from django.shortcuts import render
from .forms import CarForm, ResForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.shortcuts import render, redirect
from .models import Car, Reservation, UserData, Reg
from .forms import SignUpForm, LoginForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse


def allCars(request):
    cars = Car.objects.exclude(Reserved="Yes")
    return render(request, "team6/allcars.html", {'cars': cars})


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

            cars.user = Reg.objects.get(pk=request.session['id'])
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
                regs_count = Reg.objects.filter(username=cleaned_username).count()
                if regs_count >= 1:
                    print("-----------------------",regs_count)
                    errors.append('User Name already exists');
                else:
                    userdata.__setattr__('username',cleaned_username)
                    userdata.__setattr__('password',cleaned_password)
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
            if regs.username == usrname and regs.password == form.cleaned_data['password']:
                request.session['id'] = regs.id
                request.session['username'] = form.cleaned_data['username']
                request.session['password'] = form.cleaned_data['password']
        if(form.data['role'] == "customer"):
            return redirect('/allcars/')
        else:
            return redirect('/accounts/profile')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    logout(request)
    return render(request, "team6/form.html", {})


def delete_reservation(request, object_id):
    car = Car.objects.get(pk=object_id)
    car.Reserved = " "
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
            car.save()
            reservation.save()
            return redirect('/myreservations/')
    else:
        form = ResForm()
        car.Reserved = "Reserved"
    return render(request, "team6/resform.html", {'form': form,'car':car})

def my_reservations(request):
    reservations = Reservation.objects.all()
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
