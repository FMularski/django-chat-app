from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import widgets
from . import models


class LoginForm(AuthenticationForm):
    username = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    error_messages = {
        'invalid_login': 
            "Please enter a correct username and password. Note that both " \
            "fields may be case-sensitive."
        ,
        'inactive': "",
    }


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = 'user', 'friends', 'rooms_notifications' 

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = 'name', 

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }