from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(
        max_length=254, required=False, help_text='Optional')
    phone_number = forms.CharField(
        max_length=10, required=False,
        help_text='Optional (Format: 1234567890)')

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
