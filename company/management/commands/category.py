from django.core.management.base import BaseCommand
from company.models import CompanyCategory


class Command(BaseCommand):
    help = "Create default category objects"

    def handle(self, *args, **options):

        categories = [
            "IT",
            "Finance",
            "Marketing",
            "Sales",
            "HR",
            "Support",
            "Engineering",
            "Accounting",
            "Legal",
            "Product Management",
            "Customer Service",
            "Project Management",
            "Data Science",
            "Customer Success",
        ]

        for category in categories:
            CompanyCategory.objects.create(name=category)
            self.stdout.write(
                self.style.SUCCESS(f"Created category {category}")
            )


        self.stdout.write(
            self.style.SUCCESS("Finished saving polish cities and regions to database")
        )
