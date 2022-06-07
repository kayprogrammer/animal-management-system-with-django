from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from product.models import ShippingAddress

class RegisterForm(UserCreationForm):

    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'type':'text', 'placeholder':'Username', 'name':'user-name'}))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={'type':'email', 'placeholder':'Enter Email', 'name':'email'}))
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'type':'password', 'name':'psw', 'placeholder':'Enter Password'}))
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'type':'password', 'name':'psw-repeat', 'placeholder':'Repeat Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]

class ShippingForm(forms.ModelForm):
    countries = [
        ('Nigeria', 'Nigeria'),
        ('Ghana', 'Ghana'),
        ('South Africa', 'South Africa'),
        ('Kenya', 'Kenya'),
        ('Togo', 'Togo')
    ]
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'type':'text', 'name':'name', 'id':'name', 'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'type':'email', 'name':'email', 'style':'width:198px;', 'class':'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type':'text', 'name':'city', 'id':'city', 'class':'form-control'}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type':'text', 'name':'address', 'id':'address', 'class':'form-control'}))
    zipcode = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'type':'text', 'name':'zip', 'id':'zip', 'class':'form-control'}))
    country = forms.ChoiceField(choices=countries, widget = forms.Select(attrs={'name':'country', 'id':'country', 'class':'form-control'}))

    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['date_added']
