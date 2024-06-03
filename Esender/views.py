from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from Esender.forms import ClientForm, MailingSettingsForm, MessageForm
from Esender.models import Client, MailingSettings, Message, Logs
from users.utils import UserRequiredMixin


class HomePageView(TemplateView):
    template_name = 'Esender/base.html'


class ClientListView(LoginRequiredMixin, ListView):
    """Список клиентов"""
    model = Client

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, UserRequiredMixin, DetailView):
    """Просмотр одного клиента"""
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Класс создания клиента"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('Esender:clients')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    """Класс редактирования клиента"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('Esender:clients')


class ClientDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    """Класс удаления клиента"""
    model = Client
    success_url = 'Esender:clients'


class MailingSettingsListView(LoginRequiredMixin, ListView):
    """Класс отображения рассылок"""
    model = MailingSettings

    def get_queryset(self):
        if self.request.user.has_perm("mailing.view_all_mailings"):
            mailing_list = super().get_queryset()
        else:
            mailing_list = super().get_queryset().filter(owner_id=self.request.user)
        return mailing_list


class MailingSettingsDetailView(LoginRequiredMixin, UserRequiredMixin, DetailView):
    """Класс отображения отдельной рассылки"""
    model = MailingSettings


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    """Класс создания рассылки"""
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("Esender:settings")

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    """Класс обновления рассылки"""
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("Esender:settings")

    def get_form_class(self):
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return MailingSettingsForm
        else:
            raise Http404("У вас нет прав на редактирование рассылок")


class MailingSettingsDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    """Класс удаления рассылки"""
    model = MailingSettings
    success_url = reverse_lazy('Esender:settings')


class MessageListView(ListView):
    """Класс отображения сообщения"""
    model = Message

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Класс отображения отдельного сообщения"""
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Класс создания сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("Esender:messages")

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    """Класс редактирования сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('Esender:messages')


class MessageDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    """Класс удаления сообщения"""
    model = Message
    success_url = reverse_lazy('Esender:messages')


class LogsCreateView(CreateView):
    """Класс создания логов"""

    model = Logs

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class LogsListView(LoginRequiredMixin, ListView):
    """Класс отображения логов"""

    model = Logs

    def get_queryset(self):
        return Logs.objects.filter(user=self.request.user)
