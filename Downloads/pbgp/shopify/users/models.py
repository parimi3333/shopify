from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from django.utils import timezone

class customBaseManager(BaseUserManager):
    def _create_user(self, email, password=None, phone=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, phone=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, phone, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class customUsers(AbstractBaseUser):
    userid = models.CharField(max_length=220, unique=True)
    username = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200, blank=True, default="")
    email = models.EmailField(max_length=200, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=300)
    last_login = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    objects = customBaseManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone', 'userid']

    def __str__(self):
        return self.email

class emailverified(models.Model):
    email = models.EmailField(max_length=200)
    otp = models.IntegerField()

class Phoneverified(models.Model):
    phone = models.IntegerField()
    otp = models.IntegerField()
    
class DisplayPictures(models.Model):
    custom_user = models.ForeignKey(customUsers, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='dp/', blank=True)  # Relative to the media root

    def __str__(self):
        return f"Display Picture for {self.custom_user.username}"
