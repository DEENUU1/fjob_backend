import json
from ..models import Country, City, Region


class LoadPoland:
    def __init__(self):
        self.data = None
        self.country = "Poland"
        self.get_data()
        self.load_data()

    def get_data(self):
        with open("location/data/Poland.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def load_data(self):
        for data in self.data:
            city = data.get("Name")
            region = data.get("Province")

            country, created = Country.objects.get_or_create(name=self.country)
            region, created = Region.objects.get_or_create(name=region, country=country)
            City.objects.get_or_create(name=city, region=region)




