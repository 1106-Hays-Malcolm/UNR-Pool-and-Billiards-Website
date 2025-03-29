from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password"]

class CustomUserChangeForm(UserChangeForm):
    age = forms.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password"]
