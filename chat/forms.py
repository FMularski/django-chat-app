from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'insert username...'}))
    password = forms.CharField( widget=forms.PasswordInput(attrs={'placeholder': 'insert password...'}))
