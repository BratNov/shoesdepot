from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, AbstractUser, BaseUserManager, PermissionsMixin
from .validators import name_validators, validate_phone_number


class AppUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    object = AppUserManager()
    email = models.EmailField(null=False, blank=False, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Profile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20, null=True, blank=True, validators=name_validators)
    last_name = models.CharField(max_length=20, null=True, blank=True, validators=name_validators)
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[validate_phone_number])
    address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    is_moderator = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=AppUser)
