from offer.models import JobOffer
from celery import shared_task


@shared_task
def update_expired_offer_status():
    offers = JobOffer.objects.filter(status__in=["PENDING", "ACTIVE", "DRAFT"])
    for offer in offers:
        if offer.is_expired():
            offer.status = "EXPIRED"
            offer.save()

    print("Update JobOffer objects status")
