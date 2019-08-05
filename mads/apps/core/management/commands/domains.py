import csv
from pathlib import Path

import pytz
from django.core.management.base import LabelCommand, CommandError
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from ... import models

CURRENT_TZ = timezone.get_current_timezone()


def sort_created(value):
    return value[1]


class Command(LabelCommand):
    help = "Loads domains from the CSV file exported from an old Postfixadmin database."
    label = "file"

    @staticmethod
    def _get_datetime(value, target_timezone):
        naive = parse_datetime(value)
        return pytz.timezone(target_timezone).localize(naive, is_dst=None)

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
                    created = self._get_datetime(row[-3], options["timezone"])
                    updated = self._get_datetime(row[-2], options["timezone"])

                    data.append([row[0], created, updated, row[-1] == "1"])

            # Sort data by created time
            data.sort(key=sort_created)

            for row in data:
                _, created = models.Domain.objects.get_or_create(
                    name=row[0],
                    defaults={"created": row[1], "modified": row[2], "active": row[3]},
                )

                if not created:
                    self.stderr.write(f"Domain {row[0]} already exists")

        else:
            raise CommandError(f"File {label} does not exist")
