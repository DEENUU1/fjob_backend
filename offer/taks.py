from .models import JobOffer
from datetime import datetime
from datetime import timedelta


def delete_scraped_offers_after_30_days():
    try:
        JobOffer.objects.filter(created_at__lte=datetime.now() - timedelta(days=30)).delete()
        print("Offers deleted")
        return True
    except Exception as e:
        print(e)
        return False
