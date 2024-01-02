from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.slug_transformer import SlugTransformer
from .models import JobOffer


@receiver(post_save, sender=JobOffer)
def update_num_of_offers(sender, instance, created, **kwargs):
    # Change value of num_of_offers_to_add for company when a new job offer is created.
    if created and instance.company:
        instance.company.num_of_offers_to_add -= 1
        instance.company.save()


@receiver(post_save, sender=JobOffer)
def create_slug(sender, instance, created, **kwargs):
    # Create slug for JobOffer object based on title and id
    if created:
        transformed_title = SlugTransformer.transform(instance.title)
        instance.slug = f"{instance.id}-{transformed_title}"
        instance.save()


post_save.connect(update_num_of_offers, sender=JobOffer)
post_save.connect(create_slug, sender=JobOffer)
