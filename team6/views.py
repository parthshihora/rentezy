from django.shortcuts import render
from .forms import CarForm, ResForm
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Car, Reservation, UserData
# from .forms import UserLoginForm, UserRegisterForm, OwnerLoginForm, OwnerRegisterForm
from .forms import SignUpForm
from django.contrib.auth import views as auth_views

from django.views import generic
from django.views.generic import CreateView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse


def allCars(request):
    cars = Car.objects.all()
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
            cars.user = request.user
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
    cars = Car.objects.filter(user=request.user)
    return render(request, "team6/owner_cars.html", {'cars': cars})


def signup(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/accounts/profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, "team6/form.html", {})


def make_reservation(request, object_id):
    car = Car.objects.get(pk=object_id)
    #print "------------------------------"
    #print car.modelName
    #print "------------------------------"
    # owner = UserData.objects.get(pk=car.user)
    if request.method == 'POST':
        form = ResForm(request.POST)
        if form.is_valid():
            reservations=form.save(commit=False)
            car = Car.objects.get(pk=object_id)
            #print "------------------------------"
            #print car
            #print "------------------------------"
            #owner = UserData.objects.get(pk=car.user)
            reservation = form.save(commit=False)
            reservation.user = car.user
            reservations.save()
            return redirect('/myreservations/')
    else:
        form = ResForm()
    return render(request, "team6/resform.html", {'form': form,'car':car})

def my_reservations(request):
    reservations = Reservation.objects.all()
    print("---------------")
    print(reservations)
    print("---------------")
    return render(request, "team6/myreservations.html", {'reservations': reservations})

'''def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
	    username = form.cleaned_data.get('email')
	    password = form.cleaned_data.get('password')
	    user = authenticate(username=email,password=password)
	    login(request,user)
	    print(request.user.is_authenticated())
	    return redirect('/accounts/profile')
	return render(request,"form.html",{"form":form})'''

'''def OwnerLogin(request):
	form = OwnerLoginForm(request.POST)
	if form.is_valid():
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(username=email,password=password)
		login(request,user)
		return redirect("/home/")
	return render(request, "form.html", {'form': form})


def OwnerRegister(request):
	form = OwnerRegisterForm(request.POST)

	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.email,password=password)
		login(request,new_user)
		return redirect("/home")

	return render(request,"form.html",{"form":form})
	 




def register_view(request):
	form = UserRegisterForm(request.POST or None)

	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username,password=password)
		login(request,new_user)
		return redirect("/home")

	return render(request,"form.html",{"form":form})'''
