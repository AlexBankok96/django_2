import random
import secrets
import string

from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from catalog.forms import StyleFormMixin
from hw3.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


def logout_view(request):
    logout(request)
    return redirect('/')


class RegisterView(CreateView):
    """Регистрация нового пользователя с подтверждением через email"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(PasswordResetView, StyleFormMixin):
    """
    Контроллер для восстановления пароля
    """

    template_name = "users/reset_password.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            if user:
                password = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
                user.set_password(password)
                user.is_active = True
                user.save()
                send_mail(
                    subject="Сброс пароля",
                    message=f" Ваш новый пароль {password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            return redirect(reverse("users:login"))
        except:
            return redirect(reverse("users:register"))


class UserInValidEmail(TemplateView):
    """
    Контроллер отработки исключения, когда нет пользователя с таким email
    """

    template_name = "users/invalid_email.html"