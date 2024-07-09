from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name='Email', help_text='Введите email'
    )
    phone_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Телефон',
        help_text='Введите номер телефона'
    )
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, verbose_name='Аватар',
        help_text='Загрузите аватар'
    )
    token = models.CharField(max_length=100, blank=True, null=True, verbose_name='Токен')

    country = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Страна',
        help_text='Введите страну'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email
