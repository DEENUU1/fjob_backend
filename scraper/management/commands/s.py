from django.core.management.base import BaseCommand

from location.models import City, Country, Region, Address

data = {
    "title": "Wykładowca Game Development",
    "description": None,
    "addresses": [
        {
            "country": "Poland",
            "city": "Poznań",
            "region": None,
            "street": None
        }
    ],
    "is_remote": False,
    "is_hybrid": False,
    "apply_form": "https://justjoin.it/offers/collegium-da-vinci-wykladowca-game-development",
    "skills": ["Blender", "C++"],
    "salary": [
        {
            "salary_from": None,
            "salary_to": None,
            "currency": "PLN",
            "schedule": "MONTHLY"
        }
    ],
    "experience": [],
    "work_type": None,
    "employment_type": None,
    "company_logo": "https://public.justjoin.it/offers/company_logos/thumb_x2/66cf27f7d0028f8ede3a389745429b78aaa61588.png?1701337708",
    "url": "https://justjoin.it/offers/collegium-da-vinci-wykladowca-game-development",
    "company_name": "Collegium Da Vinci"
}


class Command(BaseCommand):
    help = "Load polish cities and regions into database"

    def handle(self, *args, **options):

        addresses = data.get("addresses")
        for address in addresses:
            country = address.get("country")
            region = address.get("region")
            city = address.get("city")
            street = address.get("street")

            country_obj, region_obj, city_obj = None, None, None

            if country:
                country_obj, created = Country.objects.get_or_create(name=country)

            if region:
                region_obj, created = Region.objects.get_or_create(name=region, country=country_obj)

            if city:
                city_obj, created = City.objects.get_or_create(name=city, region=region_obj, country=country_obj)

            Address.objects.get_or_create(country=country_obj, region=region_obj, city=city_obj, street=street)
