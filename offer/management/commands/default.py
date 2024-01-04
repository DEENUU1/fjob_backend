from django.core.management.base import BaseCommand

from offer.models import Experience, EmploymentType, WorkType


class Command(BaseCommand):
    help = "Load default Experience, Employment, WorkType objects"

    def handle(self, *args, **options):
        experiences = ["Intern", "Assistant", "Junior", "Mid", "Senior", "Expert", "C-level", "Expert", "Manager"]
        work_types = ["Part-time", "Full-time", "Freelance"]
        employment_types = ["B2B", "Permanent", "Mandate contact", "Specific-task contact"]

        for experience in experiences:
            Experience.objects.create(name=experience)

        for work_type in work_types:
            WorkType.objects.create(name=work_type)

        for employment_type in employment_types:
            EmploymentType.objects.create(name=employment_type)

        self.stdout.write(
            self.style.SUCCESS("Finished adding default values to database")
        )
