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
        parser.add_argument(
            "-i",
            "--ignore-same",
            action="store_true",
            help="Ignore aliases with same source and destination.",
        )

    def handle_label(self, label, **options):
        filepath = Path.cwd() / label

        if filepath.exists():
            data = []

            with open(label) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == row[1] and options["ignore_same"]:
                        continue

                    created = get_datetime(row[-3], options["timezone"])
                    modified = get_datetime(row[-2], options["timezone"])

                    for dest in row[1].split(","):
                        data.append(
                            # domain, source, dest., created, modified, active
                            [row[2], row[0], dest, created, modified, row[-1] == "1"]
                        )

            # Sort data by created time
            data.sort(key=sort_created)

            for row in data:
                try:
                    domain = models.Domain.objects.get(name=row[0])
                except models.Domain.DoesNotExist:
                    self.stderr.write(
                        f"Can't insert {row[1]} alias. Domain {row[0]} does not exist"
                    )
                    continue

                alias, created = models.Alias.objects.get_or_create(
                    source=row[1],
                    destination=row[2],
                    defaults={"domain": domain, "active": row[5]},
                )

                if created:
                    # Fix created and modified fields because at creation they are
                    # always set to ‘now’
                    alias.created = row[3]
                    alias.modified = row[4]
                    alias.save()
                else:
                    self.stderr.write(f"Alias {row[1]} -> {row[2]} already exists")

        else:
            raise CommandError(f"File {label} does not exist")
