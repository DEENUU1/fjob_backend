from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Statistics


@receiver(post_save, sender='users.UserAccount')
def stats_user_account(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(model_type="UserAccount")


post_save(stats_user_account, sender="users.UserAccount")


@receiver(post_save, sender='company.Company')
def stats_company(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(model_type="Company")


post_save(stats_company, sender="company.Company")


@receiver(post_save, sender='offer.JobOffer')
def stats_scraped_offer(sender, instance, created, **kwargs):
    if created and instance.is_scraped:
        Statistics.objects.create(model_type="JobOffer Scraped")


post_save(stats_scraped_offer, sender="offer.JobOffer")


@receiver(post_save, sender='offer.JobOffer')
def stats_saved_offer(sender, instance, created, **kwargs):
    if created and not instance.is_scraped:
        Statistics.objects.create(model_type="JobOffer Company")


post_save(stats_saved_offer, sender="offer.JobOffer")


@receiver(post_save, sender='support.Contact')
def stats_contact(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(model_type="Contact")


post_save(stats_contact, sender="support.Contact")


@receiver(post_save, sender='support.Report')
def stats_report(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(model_type="Report")


post_save(stats_report, sender="support.Report")
