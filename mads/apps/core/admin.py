from django.contrib import admin

from . import models


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "active"]
    list_filter = ["active"]
    search_fields = ["name"]


@admin.register(models.Mailbox)
class MailboxAdmin(admin.ModelAdmin):
    list_display = ["email", "created", "active"]
    list_filter = ["active"]
    autocomplete_fields = ["domain"]
    search_fields = ["email", "domain__name"]


@admin.register(models.Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ["source", "destination", "created", "active"]
    list_filter = ["active"]
    autocomplete_fields = ["domain"]
    search_fields = ["source", "destination", "domain__name"]
