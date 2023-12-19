from datetime import datetime
from datetime import timedelta

from .models import JobOffer


def delete_scraped_offers_after_30_days():
    try:
        JobOffer.objects.filter(is_scraped=True, created_at__lte=datetime.now() - timedelta(days=30)).delete()
        print("Offers deleted")
        return True
    except Exception as e:
        print(e)
        return False


def delete_offers_after_year():
    try:
        JobOffer.objects.filter(is_scraped=False, created_at__lte=datetime.now() - timedelta(days=365)).delete()
    except Exception as e:
        print(e)
        return False
