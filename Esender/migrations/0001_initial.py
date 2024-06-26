# Generated by Django 5.0.6 on 2024-06-18 17:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=150, unique=True, verbose_name='Почта')),
                ('name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата и время последней рассылки')),
                ('status', models.CharField(choices=[('success', 'Успешно'), ('fail', 'Не успешно')], max_length=50, verbose_name='Статус рассылки')),
                ('server_response', models.CharField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата создания рассылки')),
                ('period', models.CharField(choices=[('Раз в день', 'Раз в день'), ('Раз в неделю', 'Раз в неделю'), ('Раз в месяц', 'Раз в месяц')], max_length=50, verbose_name='Периодичность рассылки')),
                ('status', models.CharField(choices=[('Запущена', 'Запущена'), ('Создана', 'Создана'), ('Завершена', 'Завершена')], max_length=50, verbose_name='Статус')),
                ('send_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Настройка рассылки',
                'verbose_name_plural': 'Настройки рассылки',
                'permissions': [('set_deactivate', 'Can deactivate mailing'), ('view_all_mailings', 'Can view all mailing')],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Текст сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]
