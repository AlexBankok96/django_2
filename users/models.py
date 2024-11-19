from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Авторизация пользователя
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="электронный адрес")

    avatar = models.ImageField(upload_to="users/", verbose_name="аватар")
    phone = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        null=True,
        blank=True,
    )

    country = models.CharField(max_length=50, verbose_name="страна")

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email