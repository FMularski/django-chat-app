from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


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
        widget=forms.PasswordInput(attrs={'placeholder': 'enter password 1'})
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'placeholder': 'enter password 2'})
    )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'enter username...'})
        }

