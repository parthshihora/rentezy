from django import forms

from .models import CarOwner, Car

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, get_user_model,logout


User = get_user_model()


class SignUpForm(UserCreationForm):
	username = forms.CharField(max_length=30)
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
 	#password = forms.CharField(max_length=30,widget=forms.PasswordInput)
    #phone = forms.IntegerField()
    #birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

	#password = forms.CharField(max_length=30,widget=forms.PasswordInput)
	#phone = forms.IntegerField()
	#birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

	class Meta:
		model = User
		fields = ('username','first_name','last_name','email',)

class CarForm(forms.ModelForm):
	car_pic = forms.ImageField()
	'''def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		return super(CarForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		kwargs['commit']=False
		obj = super(CarForm, self).save(*args, **kwargs)
		if self.request:
			obj.user = self.request.user
		obj.save()
		return obj'''

	class Meta:
		model = Car
		fields = ['car_pic','modelNumber','modelName','regNumber','insNumber',]


		
'''class UserLoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['email','password']

	def clean(self,*args,**kwargs):
		email = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")
		if email and password:
			user = authenticate(username=email, password=password)
			if not user:
				raise forms.ValidationError("No user")
	    	if not user.check_password(password):
	    		raise forms.ValidationError("Password incorrect")
	    	if not user.is_active:
	    		raise forms.ValidationError("User not active")
		return super(UserLoginForm,self).clean(*args,**kwargs)'''

'''class OwnerLoginForm(forms.Form):
	username = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = CarOwner
		fields = ['email', 'password']
	def clean(self,*args,**kwargs):
		email = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")
		if email and password:
			user = authenticate(username=email,password=password)
			if not user:
				raise forms.ValidationError("not exist")
			if not user.check_password(password):
				raise forms.ValidationError("No pass")
			if not user.is_active():
				raise forms.ValidationError("No act")
		return super(OwnerLoginForm,self).clean(*args,**kwargs)


class OwnerRegisterForm(forms.ModelForm):
	#phone = forms.IntegerField()
	class Meta:
		model = CarOwner
		fields = ['firstName','lastname', 'email', 'password']






class UserRegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']'''



























