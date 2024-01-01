from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Company


@receiver(post_save, sender=Company)
def create_slug(sender, instance, created, **kwargs):
    # Create slug for Company object based on name and id
    if created:
        transformed_title = instance.transform_name(instance.title)
        instance.slug = f"{instance.id}-{transformed_title}"
        instance.save()


post_save.connect(create_slug, sender=Company)
