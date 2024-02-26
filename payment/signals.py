from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PaymentInfo
from .tasks import send_email


@receiver(post_save, sender=PaymentInfo)
def payment_start_notification(sender, instance, created, **kwargs):
    """
    Signal handler for sending a payment start notification email.

    Sends an email to the user when a new PaymentInfo instance is created.

    Parameters:
    - sender: The sender of the signal (PaymentInfo model in this case).
    - instance: The instance of the PaymentInfo model being saved.
    - created (bool): A flag indicating whether the instance is being created.
    - kwargs: Additional keyword arguments.

    Returns:
    - None
    """
    if created:
        subject = f"FJOB | Your payment is processing"
        message = f"Thank you for supporting this project. Soon you should get an email with payment confirm."
        send_email(subject=subject, message=message, email=instance.user.email)


post_save.connect(payment_start_notification, sender=PaymentInfo)


@receiver(post_save, sender=PaymentInfo)
def payment_success_notification(sender, instance, created, **kwargs):
    """
    Signal handler for sending a payment success notification email.

    Sends an email to the user when a PaymentInfo instance is created or updated.

    Parameters:
    - sender: The sender of the signal (PaymentInfo model in this case).
    - instance: The instance of the PaymentInfo model being saved.
    - created (bool): A flag indicating whether the instance is being created.
    - kwargs: Additional keyword arguments.

    Returns:
    - None
    """
    subject = f"FJOB | Payment success"
    message = (f"Your payment is successful, and you received {instance.product.name}. "
               f"Thank you for supporting this project. Soon you should get an email with payment confirmation. "
               )
    send_email(subject=subject, message=message, email=instance.user.email)


post_save.connect(payment_success_notification, sender=PaymentInfo)
