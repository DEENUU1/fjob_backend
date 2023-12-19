from django.core.management.base import BaseCommand

from offer.models import WorkType, EmploymentType, Experience


class Command(BaseCommand):
    help = "Create few objects for models - WorkType, EmploymentType and Experience"

    def handle(self, *args, **options):
        work_types = ['Full-time', 'Part-time', 'Internship']
        for work_type in work_types:
            try:
                WorkType.objects.create(name=work_type)
                self.stdout.write(self.style.SUCCESS(f'Created WorkType: {work_type}'))
            except Exception:
                continue

        employment_types = ['Contract of employment', 'Mandate contract', 'B2B']
        for employment_type in employment_types:
            try:
                EmploymentType.objects.create(name=employment_type)
                self.stdout.write(self.style.SUCCESS(f'Created EmploymentType: {employment_type}'))
            except Exception:
                continue

        experiences = ['Junior', 'Mid', 'Senior', 'Intern', 'Expert', 'Worker']
        for experience in experiences:
            try:
                Experience.objects.create(name=experience)
                self.stdout.write(self.style.SUCCESS(f'Created Experience: {experience}'))
            except Exception:
                continue
        self.stdout.write(self.style.SUCCESS('Command executed successfully'))
