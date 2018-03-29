from django import forms

from .models import CarOwner, Car, Reservation, Reg

from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.forms.extras.widgets import SelectDateWidget
from datetimewidget.widgets import DateTimeWidget

User = get_user_model()


# class SignUpForm(UserCreationForm):
class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    password = forms.CharField(widget=forms.PasswordInput)

    CHOICES = [('owner','Owner'),('customer','Customer')]
    role = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Reg
        fields = ('username', 'first_name', 'last_name', 'password', 'email', 'role')

class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm,self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
    password = forms.CharField(widget=forms.PasswordInput)

    CHOICES = [('owner','Owner'),('customer','Customer')]
    role = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Reg
        fields = ('username','password', 'role',)



class ResForm(forms.ModelForm):
    # pickup_date = forms.DateField(widget=AdminDateWidget())
    # drop_date = forms.DateTimeField(widget=SelectDateWidget)

    class Meta:
        model = Reservation
        widgets = {
            'pickup_date': SelectDateWidget(),
            'drop_date': SelectDateWidget()
        }
        fields = ('pickup_date', 'pickup_time', 'drop_date', 'drop_time',)


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
        fields = ['car_pic', 'modelNumber', 'modelName', 'regNumber', 'insNumber', 'priceperhour', 'pickuplocation']
