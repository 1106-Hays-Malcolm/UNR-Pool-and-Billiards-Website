from django.shortcuts import render
from django.views import View
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from accounts.models import CustomUser
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
import uuid
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        user = form.save()
        normal_users_group = Group.objects.get(name="Normal Users")
        user.groups.add(normal_users_group)

        # Generate verification URL
        token = user.verification_token
        verification_url = self.request.build_absolute_uri(
            f'/verify-email/{token}/'
        )

        # Send verification email
        subject = 'Verify your account'
        message = f'Please click the link to verify your account: {verification_url}'
        html_message = render_to_string('accounts/email_verification.html', {
            'user': user,
            'verification_url': verification_url,
        })

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )

        messages.success(self.request, 'Account created! Please check your email to verify your account.')

        return super().form_valid(form)


# Code from https://www.compilenrun.com/docs/framework/django/django-authentication/django-email-verification/
class VerifyEmailView(View):
    def get(self, request, token):
        try:
            # Convert string token to UUID
            verification_token = uuid.UUID(token)

            # Find the profile with this token
            profile = get_object_or_404(CustomUser, verification_token=verification_token)

            # Check if token is expired
            if not profile.token_is_valid():
                return render(request, 'accounts/verification_failed.html', {
                    'message': 'Verification link has expired. Please request a new one.'
                })

            # Check if already verified
            if profile.email_verified:
                return render(request, 'accounts/verification_success.html', {
                    'message': 'Your email was already verified. You can log in.'
                })

            # Verify the email
            profile.email_verified = True
            profile.save()

            return render(request, 'accounts/verification_success.html', {
                'message': 'Your email has been verified successfully! You can now log in.'
            })

        except (ValueError):
            return render(request, 'accounts/verification_failed.html', {
                'message': 'Invalid verification link.'
            })


class LoginViewWithVerifiedEmail(LoginView):
    def form_valid(self, form):
        try:
            # profile = CustomUser.objects.get(user=form.get_user())
            profile = form.get_user()
            if not profile.email_verified:
                messages.error(self.request, 'Please verify your email before logging in.')
                return redirect('accounts:login')

            return super().form_valid(form)
        except CustomUser.DoesNotExist:
            # If profile doesn't exist, create one and require verification
            profile = CustomUser.objects.create(user=form.get_user())
            messages.error(self.request, 'Please verify your email before logging in.')
            return redirect('login')
