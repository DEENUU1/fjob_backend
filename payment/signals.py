from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PaymentInfo
from .tasks import send_email


@receiver(post_save, sender=PaymentInfo)
def payment_start_notification(sender, instance, created, **kwargs):
    if created:
        subject = f"FJOB | Your payment is processing"
        message = f"Thank you for supporting this project. Soon you should get an email with payment confirm."
        send_email(subject=subject, message=message, email=instance.user.email)


post_save.connect(payment_start_notification, sender=PaymentInfo)


@receiver(post_save, sender=PaymentInfo)
def payment_success_notification(sender, instance, created, **kwargs):
    subject = f"FJOB | Payment success"
    message = (f"Your payment is successes you got {instance.product.name}. "
               f"Thank you for supporting this project. Soon you should get an email with payment confirm. "
               )
    send_email(subject=subject, message=message, email=instance.user.email)


post_save.connect(payment_success_notification, sender=PaymentInfo)
