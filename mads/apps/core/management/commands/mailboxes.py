import csv
from pathlib import Path

from django.core.management.base import LabelCommand, CommandError

from ... import models
from ._utils import get_datetime


def sort_created(value):
    return value[3]


class Command(LabelCommand):
    help = (
        "Loads mailboxes from the CSV file exported from an old Postfixadmin database."
    )
    label = "file"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "-t",
            "--timezone",
            nargs="?",
            type=str,
            default="UTC",
            help="Timezone for converting naive datetimes. Default is UTC.",
        )

    @staticmethod
    def _add_hashing_algorithm(password):
        """Method adds legacy hashing algorithm to password if it is missing."""
        return password if password[0] == "{" else f"{{MD5-CRYPT}}{password}"

    def handle_label(self, label, **options):
        filepath = Path.cwd() / label

        if filepath.exists():
            data = []

            with open(label) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    password = self._add_hashing_algorithm(row[1])
                    created = get_datetime(row[-3], options["timezone"])
                    modified = get_datetime(row[-2], options["timezone"])

                    data.append(
                        # domain, email, password, created, modified, active
                        [row[5], row[0], password, created, modified, row[-1] == "1"]
                    )

            # Sort data by created time
            data.sort(key=sort_created)

            for row in data:
                try:
                    domain = models.Domain.objects.get(name=row[0])
                except models.Domain.DoesNotExist:
                    self.stderr.write(
                        f"Can't insert {row[1]} mailbox. Domain {row[0]} does not exist"
                    )
                    continue

                mailbox, created = models.Mailbox.objects.get_or_create(
                    email=row[1],
                    defaults={"domain": domain, "password": row[2], "active": row[5]},
                )

                if created:
                    # Fix created and modified fields because at creation they are
                    # always set to ‘now’
                    mailbox.created = row[3]
                    mailbox.modified = row[4]
                    mailbox.save()
                else:
                    self.stderr.write(f"Mailbox {row[1]} already exists")
        else:
            raise CommandError(f"File {label} does not exist")
