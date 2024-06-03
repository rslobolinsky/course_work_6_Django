from django.apps import AppConfig
from django.core.management import call_command


class EsenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Esender'

    def ready(self):
        call_command('send_mailing')
