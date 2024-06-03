from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Клиент сервиса, поля email, ФИО, комментарий"""

    email = models.EmailField(max_length=150, unique=True, verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    comments = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', null=True)

    def __str__(self):
        return f'{self.name}, {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст сообщения', **NULLABLE)

    def __str__(self):
        return f'{self.title}, {self.body[:50]}...'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingSettings(models.Model):
    class PeriodMailingSettings(models.TextChoices):
        ONE_DAY = "Раз в день", _("Раз в день")
        ONE_WEEK = "Раз в неделю", _("Раз в неделю")
        ONE_MONTH = "Раз в месяц", _("Раз в месяц")

    class StatusMailingSettings(models.TextChoices):
        STARTED = "Запущена", _("Запущена")
        CREATED = "Создана", _("Создана")
        COMPLETED = "Завершена", _("Завершена")

    create_date = models.DateField(default=timezone.now, verbose_name='Дата создания рассылки')
    period = models.CharField(max_length=50, choices=PeriodMailingSettings, verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=50, choices=StatusMailingSettings, verbose_name='Статус')
    client = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    message = models.ForeignKey(Message, verbose_name='Сообщения', on_delete=models.CASCADE, related_name='Message')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец рассылки', null=True)

    def __str__(self):
        return f'{self.create_date},{self.period}, {self.status}, {self.client}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'
        permissions = [
            ("set_deactivate", "Can deactivate mailing"),
            ("view_all_mailings", "Can view all mailing"),
        ]


class Logs(models.Model):
    TRY_STATUS_TO_SEND = [
        ("success", "Успешно"),
        ("fail", "Не успешно"),
    ]

    date = models.DateField(verbose_name='Дата и время последней рассылки', auto_now_add=True)
    status = models.CharField(max_length=50, choices=TRY_STATUS_TO_SEND, verbose_name='Статус рассылки')
    server_response = models.CharField(verbose_name='Ответ почтового сервера', **NULLABLE)
    mailing_settings = models.ForeignKey(MailingSettings, verbose_name='Настройка рассылки', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.mailing_settings}, {self.date}, {self.status}, {self.user}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
