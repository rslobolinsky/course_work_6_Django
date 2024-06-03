import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserForm, UserRegisterForm
from users.models import User


class UserLogin(LoginView):
    template_name = "users/login.html"


class UserCreateView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:login")
    success_message = "Вы успешно зарегистрировались на сайте"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # не активируем пользователя
        user.save()
        # Функционал для отправки письма на почту
        token = default_token_generator.make_token(user)  # создание токена
        user.token = token
        user.save()
        uid = urlsafe_base64_encode(
            force_str(user.pk).encode()
        )  # кодирование id пользователя
        activation_url = reverse_lazy(
            "users:activate", kwargs={"uidb64": uid, "token": token}
        )
        activation_url = self.request.build_absolute_uri(activation_url)
        send_mail(
            subject="Подтверждение аккаунта",  # заголовок
            message=render_to_string(
                "users/confirm_email.html", {"activation_url": activation_url}
            ),  # сообщение
            from_email=EMAIL_HOST_USER,  # отправитель
            recipient_list=[user.email],  # получатель
            fail_silently=False,  # не пытаемся отправить письмо
        )

        return super().form_valid(form)


def activate(request, uidb64, token):
    """Подтверждение почты пользователя"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None
    if user and user.token == token:
        user.is_active = True
        user.save()
        return redirect("users:login")
    else:
        return redirect("users:email_confirmation_failed")


class VerificationFailedView(TemplateView):
    """Класс не успешной верификации"""

    template_name = "users/verification_failed.html"  # шаблон


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """обновление данных пользователя"""

    model = User
    form_class = UserForm  # форма для обновления данных
    success_url = reverse_lazy("Esender:homepage")

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    """Список всех пользователей, кроме самого себя и админа"""

    permission_required = "view_all_user"
    model = User

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .exclude(pk=self.request.user.pk)
            .exclude(is_superuser=True)
        )


def generate_new_password(request):
    new_password = "".join([str(random.randint(0, 9)) for _ in range(16)])
    new_password = make_password(new_password)
    send_mail(
        subject="Обновленный пароль",
        message=f"Используй новый пароль {new_password}",
        from_email=EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse_lazy("users:login"))  # перенаправление на страницу логина
