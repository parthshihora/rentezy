
from django.shortcuts import render
#from .forms import CarOwnerForm
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
#from .forms import UserLoginForm, UserRegisterForm, OwnerLoginForm, OwnerRegisterForm
from .forms import SignUpForm
from django.contrib.auth import views as auth_views


def owner_page(request):
	return render(request, "homepage.html")

def start_page(request):
	return render(request,"startpage.html")


def signup(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #user.refresh_from_db()
            #user.profile.birth_date = form.cleaned_data.get("birth_date")
            #user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/accounts/profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
	
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
	 

