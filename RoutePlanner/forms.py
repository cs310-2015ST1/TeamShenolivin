from django import forms
from django.contrib.auth.models import User
from RoutePlanner.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
        
class RouteForm(forms.Form):
    location1 = forms.CharField(label='Location 1', max_length=200)
    location2 = forms.CharField(label='Location 2', max_length=200)
    location3 = forms.CharField(label='Location 3', max_length=200)
    location4 = forms.CharField(label='Location 4', max_length=200)
    location5 = forms.CharField(label='Location 5', max_length=200)