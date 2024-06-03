from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from Esender.forms import StyleMixinForm
from users.models import User


class UserRegisterForm(StyleMixinForm, UserCreationForm):
    """Класс формы регистрации пользователя"""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "telephone",
            "password1",
            "password2",
        )


class UserForm(StyleMixinForm, UserChangeForm):
    """Класс формы пользователя"""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "telephone",
            "is_active",
        )  # 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()
