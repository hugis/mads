from django.contrib import admin
from django.urls import path

from . import admin_views, forms, models


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "active"]
    list_filter = ["active"]
    readonly_fields = ["created", "modified"]
    search_fields = ["name"]


@admin.register(models.Mailbox)
class MailboxAdmin(admin.ModelAdmin):
    list_display = ["email", "created", "active"]
    list_filter = ["active"]
    readonly_fields = ["created", "modified"]
    autocomplete_fields = ["domain"]
    search_fields = ["email", "domain__name"]
    form = forms.MailboxChangeForm
    add_form = forms.MailboxCreationForm

    def get_urls(self):
        return [
            path(
                "<id>/password/",
                self.admin_site.admin_view(
                    admin_views.MailboxPasswordChangeAdminView.as_view()
                ),
                name="mailbox_password_change",
            )
        ] + super().get_urls()

    def get_form(self, request, obj=None, **kwargs):
        """Use special form during mailbox creation"""

        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


@admin.register(models.Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ["source", "destination", "created", "active"]
    list_filter = ["active"]
    readonly_fields = ["created", "modified"]
    autocomplete_fields = ["domain"]
    search_fields = ["source", "destination", "domain__name"]
