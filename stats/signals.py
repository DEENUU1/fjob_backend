from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Statistics


@receiver(post_save, sender='users.UserAccount')
def stats_user_account(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(model_type="UserAccount")


@receiver(post_save, sender='candidate.Candidate')
def stats_candidate(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(model_type="Candidate")


@receiver(post_save, sender='company.Company')
def stats_candidate(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(model_type="Company")


@receiver(post_save, sender='offer.JobOffer')
def stats_scraped_offer(sender, instance, created, **kwargs):
    if created and instance.is_scraped:
        Statistics.objects.create(model_type="JobOffer Scraped")


@receiver(post_save, sender='offer.JobOffer')
def stats_saved_offer(sender, instance, created, **kwargs):
    if created and not instance.is_scraped:
        Statistics.objects.create(model_type="JobOffer Company")


@receiver(post_save, sender='support.Contact')
def stats_contact(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(model_type="Contact")


@receiver(post_save, sender='support.Report')
def stats_report(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(model_type="Report")
