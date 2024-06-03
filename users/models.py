from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    """Класс пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта", max_length=254)  # email
    first_name = models.CharField(max_length=30, verbose_name="Имя", **NULLABLE)
    last_name = models.CharField(max_length=30, verbose_name="Фамилия", **NULLABLE)
    telephone = models.CharField(max_length=20, unique=True, verbose_name="Телефон", **NULLABLE)  # телефон

    token = models.CharField(max_length=255, **NULLABLE)

    USERNAME_FIELD = "email"  # имя пользователя
    REQUIRED_FIELDS = []  # обязательные поля

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = (
            ("set_user_deactivate", "Can deactivate user"),
            ("view_all_user", "Can view all user"),
        )

    def __str__(self):
        return f"{self.email}, {self.first_name}, {self.last_name}"
