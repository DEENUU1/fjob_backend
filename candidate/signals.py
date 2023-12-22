from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Candidate
from .tasks import send_email


@receiver(post_save, sender=Candidate)
def applied_email_notification(sender, instance, created, **kwargs):
    if created:
        subject = f"FJOB | Thank you for applying to {instance.offer.title}"
        message = f"Congratulations your application has been sent."
        send_email(subject=subject, message=message, email=instance.email)


post_save.connect(applied_email_notification, sender=Candidate)


@receiver(post_save, sender=Candidate)
def status_updated_notification(sender, instance, created, **kwargs):
    subject = f"FJOB | Your application status has changed."
    message = f"Your application status has been updated to {instance.status}"
    send_email(subject=subject, message=message, email=instance.email)


post_save.connect(status_updated_notification, sender=Candidate)
