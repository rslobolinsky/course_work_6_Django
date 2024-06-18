import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db.models import F
from django_apscheduler.jobstores import DjangoJobStore

from config import settings
from Esender.models import Logs, MailingSettings, Message


class Command(BaseCommand):
    """Класс для запуска APScheduler."""

    help = "Runs APScheduler."

    @staticmethod
    def send_mailing() -> None:
        """Отправляет письмо."""
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        mailing = MailingSettings.objects.filter(
            send_time__lte=current_datetime
        ).filter(status__in=[MailingSettings.StatusMailingSettings.CREATED])

        for mailing in mailing:
            try:
                send_mail(
                    subject=Message.objects.get(id=mailing.id).title,
                    message=Message.objects.get(id=mailing.id).body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.client.all()],
                )
                if (
                    mailing.period == MailingSettings.PeriodMailingSettings.ONE_DAY
                    and current_datetime.day >= 1
                ):
                    mailing.sent_time = F("sent_time") + timedelta(days=1)
                    mailing.status = MailingSettings.StatusMailingSettings.STARTED
                elif (
                    mailing.period == MailingSettings.PeriodMailingSettings.ONE_WEEK
                    and current_datetime.day >= 7
                ):
                    mailing.sent_time = F("sent_time") + timedelta(days=7)
                    mailing.status = MailingSettings.StatusMailingSettings.STARTED
                elif (
                    mailing.period == MailingSettings.PeriodMailingSettings.ONE_MONTH
                    and current_datetime.day >= 30
                ):
                    mailing.sent_time = F("sent_time") + timedelta(days=30)
                    mailing.status = MailingSettings.StatusMailingSettings.STARTED
                mailing.save()
                status = True
                server_response = "Успешно"
            except smtplib.SMTPResponseException as e:
                status = False
                server_response = str(e)
            finally:
                Logs.objects.create(
                    mailing_settings=mailing,
                    status=status,
                    server_response=server_response,
                )

    def handle(self, *args, **options) -> None:
        """Запускает APScheduler."""
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(self.send_mailing, "interval", seconds=10)
        scheduler.start()

