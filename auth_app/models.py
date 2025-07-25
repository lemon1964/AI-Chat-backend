# backend/auth_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    provider = models.CharField(max_length=50, default='credentials', blank=True, null=True)
    points = models.IntegerField(default=0)
    
    # Указываем, что логин происходит через email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Поля, которые обязательно запрашиваются при создании superuser

    objects = CustomUserManager()  # Подключаем кастомный менеджер
    def __str__(self):
        return self.email

