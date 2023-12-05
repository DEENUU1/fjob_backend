import pytest
from location.models import Country, Region, City, Address


@pytest.mark.django_db
def test_create_country_success():
    country = Country.objects.create(name='Poland')
    assert country.name == 'Poland'


@pytest.mark.django_db
def test_create_region_success():
    country = Country.objects.create(name='Poland')
    region = Region.objects.create(name='Warsaw', country=country)
    assert region.name == 'Warsaw'
    assert region.country == country


@pytest.mark.django_db
def test_create_city_success():
    country = Country.objects.create(name='Poland')
    region = Region.objects.create(name='Warsaw', country=country)
    city = City.objects.create(name='Warsaw', region=region, country=country)
    assert city.name == 'Warsaw'
    assert city.region == region
    assert city.country == country


@pytest.mark.django_db
def test_create_address_success():
    country = Country.objects.create(name='Poland')
    region = Region.objects.create(name='Warsaw', country=country)
    city = City.objects.create(name='Warsaw', region=region, country=country)
    address = Address.objects.create(city=city, street="Złota 44", country=country, region=region)
    assert address.city == city
    assert address.street == "Złota 44"
    assert address.country == country
    assert address.region == region
