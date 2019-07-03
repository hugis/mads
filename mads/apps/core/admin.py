from django.contrib import admin

from . import models


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["domain", "created", "active"]
    list_filter = ["active"]
    search_fields = ["domain"]
