from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Клиент сервиса, поля email, ФИО, комментарий"""

    email = models.EmailField(max_length=150, unique=True, verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    comments = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.name}, {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текс сообщения', **NULLABLE)

    def __str__(self):
        return f'{self.title}, {self.body[:50]}...'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingSettings(models.Model):
    """Класс рассылки, поля дата и время, периодичность(раз в день, раз в неделю, раз в месяц),
    статус рассылки(завершена, создана, запущена)
    """

    class PeriodMailingSettings(models.TextChoices):
        ONE_DAY = "Раз в день", _("Раз в день")
        ONE_WEEK = "Раз в неделю", _("Раз в неделю")
        ONE_MONTH = "Раз в месяц", _("Раз в месяц")

    class StatusMailingSettings(models.TextChoices):
        STARTED = "Запущена", _("Запущена")
        CREATED = "Создана", _("Создана")
        COMPLETED = "Завершена", _("Завершена")

    date_and_time = models.DateField(verbose_name='Дата и время первой рассылки')
    period = models.CharField(max_length=50, choices=PeriodMailingSettings, verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=50, choices=StatusMailingSettings, verbose_name='Статус')
    client = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    message = models.ForeignKey(Message, verbose_name='Сообщения', on_delete=models.CASCADE, related_name='Message')

    def __str__(self):
        return f'{self.date_and_time},{self.period}, {self.status}, {self.client}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'


class Logs(models.Model):
    """Модель попытки рассылки, поля: дата и время последней рассылки, статус(успешно/не успешно)
    ответ почтового сервера, если он был
    """
    date = models.DateField(verbose_name='Дата и время последней рассылки', auto_now_add=True)
    status = models.BooleanField(verbose_name='Статус рассылки')
    server_response = models.CharField(verbose_name='Ответ почтового сервера', **NULLABLE)
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE)

    # client = models.ForeignKey(Client, verbose_name='клиент', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}, {self.status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
