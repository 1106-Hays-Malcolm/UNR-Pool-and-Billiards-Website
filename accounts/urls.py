from django.urls import path

from .views import SignUpView
from django.contrib.auth import views as auth_views

app_name = "accounts"
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="accounts/password_change_form.html"), name="password_change"),
    path("password_change_done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_change_done.html"), name="password_change_done"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name="logout")
]