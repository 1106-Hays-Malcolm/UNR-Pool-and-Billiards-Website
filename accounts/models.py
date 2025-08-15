from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        if not first_name:
            raise ValueError("Users must have a fist name")
        
        if not last_name:
            raise ValueError("Users must have a last name")
        
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractUser):
    
    username = None
    email = models.EmailField(unique=True, max_length=255)

    objects = MyUserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        permissions = [
            ("can_view_officers_list", "Can view the list of officer. Captains should have this permission."),
            ("can_manage_officer_status", "Can give or revoke the officer status from users. Captains should have this permission."),
            ("eligible_to_be_officer", "Is eligible to become an officer. Regular users should be eligible, but not current officers or captains."),
            ("able_to_be_demoted_as_officer", "Is able to be demoted as an officer. Officers should have this permission."),
            ("able_to_be_demoted_as_captain", "Is able to be demoted as a captain. Captains should have this permission."),
            ("eligible_to_be_captain", "Is eligible to become a captain. Only officers should be eligible."),
            ("can_manage_captain_status", "Can give or revoke captain status from users. Only the president should have this permission")
        ]
