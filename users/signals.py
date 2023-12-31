from django.db.models.signals import post_save
from django.dispatch import receiver

from company.models import Company
from users.models import UserAccount


@receiver(post_save, sender=UserAccount)
def create_company(sender, instance, created, **kwargs):
    if created:
        if instance.account_type == "COMPANY":
            Company.objects.create(name=f"{hash(instance.email)}", user=instance)


post_save.connect(create_company, sender=UserAccount)
