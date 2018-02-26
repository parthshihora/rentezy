
from django.shortcuts import render
from .forms import CarForm
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Car
#from .forms import UserLoginForm, UserRegisterForm, OwnerLoginForm, OwnerRegisterForm
from .forms import SignUpForm
from django.contrib.auth import views as auth_views

from django.views import generic
from django.views.generic import CreateView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse




def objectDelete(request, object_id):
	print("*****",object_id)
	object = get_object_or_404(Car, pk=object_id)
	object.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	#redirect('/yourcars/')

def modifyCar(request,object_id):
	#object = get_object_or_404(Car, pk=object_id)
	if request.POST:
		form = CarForm(request.POST,request.FILES)
		if form.is_valid():
			car = Car.objects.get(pk=object_id)
			car.car_pic = request.FILES.get("car_pic")
			form = CarForm(request.POST,instance=car)
			form.save()
			return HttpResponseRedirect('/yourcars/')
	else:
		#car = Car.objects.get(pk = object_id)       
		#form = CarForm(instance=car)
		form = CarForm()


	#print("****Modify",object.modelNumber)
	#return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	return render(request, "carform.html",{'form':form})


def owner_profile(request):
	return render(request, "ownerprofile.html")

def add_car(request):   # carentry car instead of this
	if request.method == "POST":
		form = CarForm(request.POST,request.FILES);
		if form.is_valid():
			cars = form.save(commit=False)
			cars.user = request.user
			cars.car_pic = request.FILES.get("car_pic")
			cars.save()
			#form.save()
			return redirect('/yourcars/')
	else:
		form = CarForm()
	return render(request, "carform.html",{'form':form})


def start_page(request):
	return render(request,"startpage.html")

def your_cars(request): # CarView class instead of this
	#user = Car.user
	cars = Car.objects.filter(user=request.user)
	return render(request,"team6/owner_cars.html",{'cars':cars})




def signup(request):
	if request.method == 'POST':
        #form = UserCreationForm(request.POST)
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
			user = form.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			return redirect('/accounts/profile')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

def logout_view(request):
	logout(request)
	return render(request,"team6/form.html",{})
	
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
	 

