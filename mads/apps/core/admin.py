from django.contrib import admin
from django.urls import path

from . import admin_views, forms, models

admin.site.site_header = "Mailbox administration"


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "active"]
    list_filter = ["active"]
    readonly_fields = ["created", "modified"]
    search_fields = ["name"]


@admin.register(models.Mailbox)
class MailboxAdmin(admin.ModelAdmin):
    list_display = ["email", "created", "active", "_quota"]
    list_filter = ["active"]
    readonly_fields = ["created", "modified"]
    autocomplete_fields = ["domain"]
    search_fields = ["email", "domain__name"]
    form = forms.MailboxChangeForm
    add_form = forms.MailboxCreationForm

    def _quota(self, obj):
        if obj.quota == 0:
            return "∞"
        else:
            suffix = obj.get_quota_suffix_display() if obj.quota_suffix else "KiB"
            return f"{obj.quota} {suffix}"

    _quota.short_description = "Quota"

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
