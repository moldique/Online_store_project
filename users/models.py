from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя с дополнительными полями"""
    
    # Переопределяем поле авторизации на email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # Дополнительные поля
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        help_text='Обязательное поле. Используется для входа в систему.'
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='users/avatars/',
        blank=True,
        null=True,
        help_text='Загрузите изображение для аватара'
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
        blank=True,
        null=True,
        help_text='Введите номер телефона'
    )
    country = models.CharField(
        verbose_name='Страна',
        max_length=100,
        blank=True,
        null=True,
        help_text='Введите название страны'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f'{self.email}'
