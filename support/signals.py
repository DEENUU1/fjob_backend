from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Contact
from .tasks import send_email


@receiver(post_save, sender=Contact)
def contact_sent_notification(sender, instance, created, **kwargs):
    if created:
        subject = f"FJOB | Thank you for contacting with us."
        message = f"Thank you for contacting us, we will try to answer your question as soon as possible"
        try:
            send_email(subject=subject, message=message, email=instance.email)
        except Exception as e:
            pass


post_save.connect(contact_sent_notification, sender=Contact)
