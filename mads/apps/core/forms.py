from typing import Optional

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext as _

from . import models


class MailboxCreationForm(forms.ModelForm):
    error_messages = {
        "duplicate_email": _("A mailbox with that email already exists."),
        "password_mismatch": _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        label=_("Password"), strip=False, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )

    class Meta:
        model = models.Mailbox
        fields = ["domain", "email", "active"]

    def clean_email(self):
        # Since Mailbox.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM.
        email = self.cleaned_data["email"]
        try:
            # noinspection PyProtectedMember
            models.Mailbox.objects.get(email=email)
        except models.Mailbox.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"], code="duplicate_email"
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password_mismatch"
            )
        return password2

    def save(self, commit=True):
        mailbox = super().save(commit=False)
        return mailbox.set_password(self.cleaned_data["password1"], commit)


class ReadOnlyPasswordWidget(forms.Widget):
    template_name = "auth/widgets/read_only_password_hash.html"
    read_only = True

    @staticmethod
    def _get_algorithm(first_component: str) -> Optional[str]:
        if len(first_component) == 0:
            return None

        if first_component[0] == "{":
            return first_component[1:-1]
        elif first_component == "1":
            return "SHA256-CRYPT"
        elif first_component == "1":
            return "MD5-CRYPT"
        else:
            return None

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []

        hash_components = value.split("$")
        algorithm = self._get_algorithm(hash_components[0])

        if algorithm:
            summary.append({"label": _("Hash algorithm"), "value": algorithm})
            if algorithm == "SHA256-CRYPT":
                summary.append(
                    {"label": _("Rounds"), "value": hash_components[-3].split("=")[1]}
                )
            summary.append({"label": _("Salt"), "value": hash_components[-2]})
            summary.append({"label": _("Hash"), "value": hash_components[-1]})
        else:
            summary.append({"label": _("Unknown hash algorithm"), "value": value})

        context["summary"] = summary
        return context


class ReadOnlyPasswordField(ReadOnlyPasswordHashField):
    widget = ReadOnlyPasswordWidget


class MailboxChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "password, but you can change the password using "
            '<a href="../password/">this form</a>.'
        ),
    )

    class Meta:
        model = models.Mailbox
        fields = "__all__"

    def clean_password(self):
        return self.initial["password"]


class MailboxSetPasswordForm(forms.Form):
    """A form that lets a user set password for a mailbox."""

    error_messages = {"password_mismatch": _("The two password fields didn't match.")}
    new_password1 = forms.CharField(
        label=_("New password"), widget=forms.PasswordInput, strip=False
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"), strip=False, widget=forms.PasswordInput
    )

    def __init__(self, mailbox, *args, **kwargs):
        self.mailbox = mailbox
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages["password_mismatch"], code="password_mismatch"
                )
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.mailbox.set_password(password)
        if commit:
            self.mailbox.save()
        return self.mailbox
