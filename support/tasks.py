from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_email(email, subject, message):
    """
    Celery task for sending an email.

    Parameters:
    - email (str): The recipient email address.
    - subject (str): The subject of the email.
    - message (str): The content of the email.

    Returns:
    - None
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email]
    )
