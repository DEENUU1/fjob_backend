from django.core.management.base import BaseCommand

from location.parser.poland import LoadPoland


class Command(BaseCommand):
    help = "Load polish cities and regions into database"

    def handle(self, *args, **options):
        LoadPoland()

        self.stdout.write(
            self.style.SUCCESS("Finished saving polish cities and regions to database")
        )
