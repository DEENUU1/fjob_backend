from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "Load default products"

    def handle(self, *args, **options):


        self.stdout.write(
            self.style.SUCCESS("Finished saving polish cities and regions to database")
        )
