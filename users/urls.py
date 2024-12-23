from django.contrib.auth.views import LoginView
from django.urls import path

from users.apps import UsersConfig
from users.views import logout_view, RegisterView, ProfileView, email_verification, UserPasswordResetView, \
    UserInValidEmail

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('reset-password/', UserPasswordResetView.as_view(), name='reset_password'),
    path("invalid-email/", UserInValidEmail.as_view(), name="invalid_email"),
]