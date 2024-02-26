from django.db.models.signals import post_save
from django.dispatch import receiver

from company.models import Company
from users.models import UserAccount


@receiver(post_save, sender=UserAccount)
def create_company(sender, instance, created, **kwargs):
    """
    Signal handler for creating a Company instance when a new UserAccount is created.

    Parameters:
    - sender: The sender of the signal (UserAccount model in this case).
    - instance: The instance of the UserAccount model being saved.
    - created (bool): A flag indicating whether the instance is being created.
    - kwargs: Additional keyword arguments.

    Returns:
    - None
    """
    if created:
        if instance.account_type == "COMPANY":
            Company.objects.create(name=f"{hash(instance.email)}", user=instance)


post_save.connect(create_company, sender=UserAccount)
