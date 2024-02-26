from offer.models import JobOffer
from celery import shared_task


@shared_task
def update_expired_offer_status():
    """
    Celery task for updating the status of expired JobOffer objects.

    Retrieves JobOffer objects with status "PENDING", "ACTIVE", or "DRAFT" and updates the status to "EXPIRED"
    if the offer is expired.

    Returns:
    - None
    """

    offers = JobOffer.objects.filter(status__in=["PENDING", "ACTIVE", "DRAFT"])
    for offer in offers:
        if offer.is_expired():
            offer.status = "EXPIRED"
            offer.save()

    print("Update JobOffer objects status")
