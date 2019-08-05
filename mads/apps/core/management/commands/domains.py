import csv
from pathlib import Path

from django.core.management.base import LabelCommand, CommandError
from django.utils import timezone

from ... import models
from ._utils import get_datetime

CURRENT_TZ = timezone.get_current_timezone()


def sort_created(value):
    return value[1]


class Command(LabelCommand):
    help = "Loads domains from the CSV file exported from an old Postfixadmin database."
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

    def handle_label(self, label, **options):
        filepath = Path(__file__).parent / label

        if filepath.exists():
            data = []

            with open(label) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    created = get_datetime(row[-3], options["timezone"])
                    modified = get_datetime(row[-2], options["timezone"])

                    #            name,   created, modified, active
                    data.append([row[0], created, modified, row[-1] == "1"])

            # Sort data by created time
            data.sort(key=sort_created)

            for row in data:
                domain, created = models.Domain.objects.get_or_create(
                    name=row[0],
                    defaults={"created": row[1], "modified": row[2], "active": row[3]},
                )

                if created:
                    # Fix created and modified fields because at creation they are
                    # always set to ‘now’
                    domain.created = row[1]
                    domain.modified = row[2]
                    domain.save()
                else:
                    self.stderr.write(f"Domain {row[0]} already exists")

        else:
            raise CommandError(f"File {label} does not exist")
