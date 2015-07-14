from django import forms
from django.contrib.auth.models import User
from RoutePlanner.models import UserProfile, Route

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
        
class RouteForm(forms.ModelForm):
    location1 = forms.CharField(label='Location 1', max_length=200, required=False)
    location2 = forms.CharField(label='Location 2', max_length=200, required=False)
    location3 = forms.CharField(label='Location 3', max_length=200, required=False)
    location4 = forms.CharField(label='Location 4', max_length=200, required=False)
    location5 = forms.CharField(label='Location 5', max_length=200, required=False)
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Route
        fields = ('location1', 'location2', 'location3', 'location4', 'location5')