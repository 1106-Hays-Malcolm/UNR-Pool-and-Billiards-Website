from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = [
        ("Email Address", {"fields": ["email"]}),
        ("First Name", {"fields": ["first_name"]}),
        ("Last Name", {"fields": ["last_name"]}),
        ("Groups", {"fields": ["groups"]})
    ]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    ordering = ["last_name"]

admin.site.register(CustomUser, CustomUserAdmin)