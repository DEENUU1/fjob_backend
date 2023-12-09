from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PaymentInfo
from .tasks import send_email_task


@receiver(post_save, sender=PaymentInfo)
def send_payment_created_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Payment Created'
        message = f'Hello {instance.user.username}, your payment for {instance.product} has been created.'

        send_email_task([instance.user.email], subject, message)


@receiver(post_save, sender=PaymentInfo)
def send_payment_completed_email(sender, instance, **kwargs):
    if instance.payment_bool:
        subject = 'Payment Completed'
        message = f'Hello {instance.user.username}, your payment for {instance.product} has been completed.'

        send_email_task([instance.user.email], subject, message)
