from django.contrib import admin

from Esender.models import Client


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email')
    list_filter = ('name',)
    search_fields = ('name', 'email', 'comments')