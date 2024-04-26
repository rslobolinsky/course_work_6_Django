from Esender.apps import EsenderConfig
from django.urls import path
from Esender.views import HomePageView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailingSettingsListView, MailingSettingsDetailView, MailingSettingsCreateView, MailingSettingsUpdateView, \
    MailingSettingsDeleteView

app_name = EsenderConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('create/', ClientCreateView.as_view(), name='create-client'),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='delete-client'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message-update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message-delete'),

    path('settings/', MailingSettingsListView.as_view(), name='settings'),
    path('settings/<int:pk>/', MailingSettingsDetailView.as_view(), name='settings-detail'),
    path('settings/create/', MailingSettingsCreateView.as_view(), name='settings-create'),
    path('settings/update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='setting-update'),
    path('settings/delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='setting-delete')
]

