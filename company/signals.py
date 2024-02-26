from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.slug_transformer import SlugTransformer
from .models import Company


@receiver(post_save, sender=Company)
def create_slug(sender, instance, created, **kwargs) -> None:
    """
    Signal handler to create a slug for a Company object based on its name and id.

    Parameters:
    - sender: The sender of the signal (Company model in this case).
    - instance: The instance of the Company model being saved.
    - created (bool): A flag indicating whether the instance is being created.
    - kwargs: Additional keyword arguments.

    Returns:
    - None
    """
    if created:
        transformed_name = SlugTransformer.transform(instance.name)
        instance.slug = f"{instance.id}-{transformed_name}"
        instance.save()


post_save.connect(create_slug, sender=Company)
