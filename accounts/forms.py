from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]
