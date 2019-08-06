from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from . import forms, models


class MailboxPasswordChangeAdminView(FormView):
    form_class = forms.MailboxSetPasswordForm
    template_name = "core/mailbox_password_change_form.html"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # noinspection PyAttributeOutsideInit
        self.mailbox = get_object_or_404(models.Mailbox, pk=kwargs["id"])
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["mailbox"] = self.mailbox
        return kwargs

    def get_success_url(self):
        content_type = ContentType.objects.get_for_model(self.mailbox)
        return reverse(
            f"admin:{content_type.app_label}_{content_type.model}_change",
            args=[self.mailbox.pk],
        )

    def form_valid(self, form):
        mailbox = form.save()
        messages.success(self.request, f"The password for {mailbox} has been changed.")
        return super().form_valid(form)
