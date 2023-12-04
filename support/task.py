from .models import Contact, Report
from datetime import datetime
from datetime import timedelta


def delete_contact_after_year():
    try:
        Contact.objects.filter(created_at__lte=datetime.now() - timedelta(days=365)).delete()
        return True
    except Exception as e:
        print(e)
        return False


def delete_report_after_year():
    try:
        Report.objects.filter(created_at__lte=datetime.now() - timedelta(days=365)).delete()
        return True
    except Exception as e:
        print(e)
        return False
