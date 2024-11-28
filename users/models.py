from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    """
    Авторизация пользователя
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="электронный адрес")

    avatar = models.ImageField(upload_to="users/", verbose_name="аватар", blank=True, null=True)
    phone = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        null=True,
        blank=True,
    )

    country = models.CharField(max_length=50, verbose_name="страна", blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    date_joined = models.DateTimeField(default=now, verbose_name="Дата регистрации")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Добавление related_name для groups и user_permissions
    groups = models.ManyToManyField(
        'auth.Group', related_name='users_user_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='users_user_permissions_set', blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
