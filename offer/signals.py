from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.slug_transformer import SlugTransformer
from .models import JobOffer


@receiver(post_save, sender=JobOffer)
def update_num_of_offers(sender, instance, created, **kwargs):
    """
    Signal receiver to update the num_of_offers_to_add for the company when a new JobOffer is created.

    Args:
    - sender: The sender of the signal.
    - instance: The instance of the JobOffer.
    - created: A boolean indicating whether the instance was created.
    - kwargs: Additional keyword arguments.

    Action:
    - Decreases the num_of_offers_to_add for the associated company when a new JobOffer is created.
    """
    if created and instance.company:
        instance.company.num_of_offers_to_add -= 1
        instance.company.save()


@receiver(post_save, sender=JobOffer)
def create_slug(sender, instance, created, **kwargs):
    """
    Signal receiver to create a slug for the JobOffer object based on its title and id when it is created.

    Args:
    - sender: The sender of the signal.
    - instance: The instance of the JobOffer.
    - created: A boolean indicating whether the instance was created.
    - kwargs: Additional keyword arguments.

    Action:
    - Creates a slug for the JobOffer object based on its title and id when it is created.
    """
    if created:
        transformed_title = SlugTransformer.transform(instance.title)
        instance.slug = f"{instance.id}-{transformed_title}"
        instance.save()


# Connect the signal receivers to the JobOffer model
post_save.connect(update_num_of_offers, sender=JobOffer)
post_save.connect(create_slug, sender=JobOffer)
