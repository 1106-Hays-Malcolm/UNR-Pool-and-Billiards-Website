from django.shortcuts import render

# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from accounts.models import CustomUser
from django.contrib.auth.models import Group

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        user = form.save()
        normal_users_group = Group.objects.get(name="Normal Users")
        user.groups.add(normal_users_group)

        return super().form_valid(form)
