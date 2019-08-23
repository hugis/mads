from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _

from ... import models


class Command(BaseCommand):
    help = "Sends warning message to user whose mailbox over a limit."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "email", type=str, help="A name of mailbox which has a limit problem."
        )
        parser.add_argument(
            "percent", type=int, help="A warning limit which has been crossed."
        )

    def handle(self, *args, **options):
        try:
            mailbox = models.Mailbox.objects.get(email=options["email"])
        except models.Mailbox.DoesNotExist:
            raise CommandError(f"Uknown mailbox: {options['email']}")

        subject = f"{settings.EMAIL_SUBJECT_PREFIX}{_('Quota warning')}"
        msg = _("Your mailbox is now {}% full.").format(options["percent"])

        send_mail(
            subject,
            msg,
            settings.DEFAULT_FROM_EMAIL,
            [mailbox.email],
            fail_silently=True,
        )
