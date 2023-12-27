from django.core.management.base import BaseCommand
from payment.models import Product
from django.conf import settings


class Command(BaseCommand):
    help = "Load default products"

    def handle(self, *args, **options):

        # product 1
        Product.objects.create(
            type="NEW_OFFER",
            name="Basic",
            value=1,
            price_euro=0,
            price_euro_id=settings.PRICE_BASIC,
        )
        # product 2
        Product.objects.create(
            type="NEW_OFFER",
            name="Standard",
            value=5,
            price_euro=10,
            price_euro_id=settings.PRICE_STANDARD,
        )
        # product 3
        Product.objects.create(
            type="NEW_OFFER",
            name="Advanced",
            value=10,
            price_euro=25,
            price_euro_id=settings.PRICE_ADVANCED,
        )
        self.stdout.write(self.style.SUCCESS("Finished saving products to database"))

