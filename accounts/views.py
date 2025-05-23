from django.shortcuts import render

# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.contrib.auth.models import Group
from accounts.models import CustomUser

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

class ListCaptainsView(ListView):
    template_name = "accounts/captain_list.html"
    context_object_name = "captain_list"

    def get_queryset(self):
        captain_group = Group.objects.get(name="Officers")
        captain_list = CustomUser.objects.get(groups=captain_group)

        return captain_list