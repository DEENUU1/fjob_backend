from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Contact
from .tasks import send_email


@receiver(post_save, sender=Contact)
def contact_sent_notification(sender, instance, created, **kwargs):
    """
    Signal handler for sending a contact sent notification email.

    Sends an email to the contact when a new Contact instance is created.

    Parameters:
    - sender: The sender of the signal (Contact model in this case).
    - instance: The instance of the Contact model being saved.
    - created (bool): A flag indicating whether the instance is being created.
    - kwargs: Additional keyword arguments.

    Returns:
    - None
    """
    if created:
        subject = f"FJOB | Thank you for contacting with us."
        message = f"Thank you for contacting us, we will try to answer your question as soon as possible"
        try:
            send_email(subject=subject, message=message, email=instance.email)
        except Exception as e:
            pass


post_save.connect(contact_sent_notification, sender=Contact)
