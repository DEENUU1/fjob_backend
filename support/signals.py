from django.dispatch import receiver
from .models import Contact
from .tasks import send_email
from django.db.models.signals import post_save


@receiver(post_save, sender=Contact)
def contact_sent_notification(sender, instance, created, **kwargs):
    if created:
        subject = f"FJOB | Thank you for contacting with us."
        message = f"Thank you for contacting us, we will try to answer your question as soon as possible"
        send_email(subject=subject, message=message, email=instance.email)