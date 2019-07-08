from django.contrib import admin

from . import models


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["domain", "created", "active"]
    list_filter = ["active"]
    search_fields = ["domain"]


@admin.register(models.Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ["address", "created", "active"]
    list_filter = ["active"]
    search_fields = ["address", "domain"]


@admin.register(models.Mailbox)
class MailboxAdmin(admin.ModelAdmin):
    list_display = ["username", "created", "active"]
    list_filter = ["active"]
    search_fields = ["username", "domain"]
