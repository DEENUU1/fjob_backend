from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Candidate
from .tasks import send_email


@receiver(post_save, sender=Candidate)
def send_status_change_email(sender, instance, **kwargs):
    if kwargs["created"]:
        return

    if instance.status != instance._original_status:
        subject = "Application status changed"
        message = f"Your application status has changed to {instance.status} for offer {instance.offer.title}"
        send_email.delay(subject, message, [instance.email])


@receiver(post_save, sender=Candidate)
def send_success_application_notification(sender, instance, **kwargs):
    if not kwargs["created"]:
        return

    subject = "Thank you for applying!"
    message = f"Thank you for applying to {instance.offer.title}. We will contact you soon!"
    send_email.delay(subject, message, [instance.email])


