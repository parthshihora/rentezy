from django import forms

from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.forms.extras.widgets import SelectDateWidget
#from datetimewidget.widgets import DateTimeWidget

User = get_user_model()


class OwnerSignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OwnerSignUpForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
            if self.fields[key] == 'role':
                self.fields[key].type == 'hidden'

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Reg_Owner
        fields = ('username', 'first_name', 'last_name', 'password', 'email',)


class CustomerSignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm,self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Reg_Customer
        fields = ('username', 'first_name', 'last_name', 'password', 'email',)


class OwnerLoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OwnerLoginForm,self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Reg_Owner
        fields = ('username','password',)

class CustomerLoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerLoginForm,self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Reg_Customer
        fields = ('username','password',)


class AdminLoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminLoginForm,self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Reg_Admin
        fields = ('username','password',)


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
    CARTYPES = [('none', 'No Filter'), ('compact', 'Compact'), ('sedan','Sedan'),('suv','SUV')]
    NOP = [('0', 'No Filter'), ('4', '4'), ('5', '5'), ('6', '6'), ('7','7')]
    cartype = forms.ChoiceField(choices=CARTYPES,label='cartype')
    passengerCapacity = forms.ChoiceField(choices=NOP,label='passengerCapacity')
    class Meta:
        model = Car
        fields = ['car_pic', 'modelNumber', 'modelName', 'regNumber', 'insNumber', 'priceperhour', 'pickuplocation','cartype','passengerCapacity']


class FilterForm(forms.ModelForm):
    CARTYPES = [('none', 'No Filter'), ('compact', 'Compact'), ('sedan','Sedan'),('suv','SUV')]
    NOP = [('0', 'No Filter'), ('4', '4'), ('5', '5'), ('6', '6'), ('7','7')]
    cartype = forms.ChoiceField(choices=CARTYPES,label='cartype')
    passengerCapacity = forms.ChoiceField(choices=NOP,label='passengerCapacity')
    class Meta:
        model = Car
        fields = ['cartype', 'passengerCapacity']


class UserFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserFeedbackForm,self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Feedback
        fields = ('message', 'rating',)
