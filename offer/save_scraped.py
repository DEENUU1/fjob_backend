from typing import Dict, Any

from location.models import City, Region, Country, Address
from offer.models import JobOffer, EmploymentType, WorkType, Experience, Salary


def save_scraped(data: Dict[str, Any]) -> None:
    # Process and create objects based on given data from scrapers
    title = data.get("title")
    description = data.get("description")
    is_remote = data.get("is_remote")
    is_hybrid = data.get("is_hybrid")
    skills = data.get("skills")
    salaries = data.get("salary")
    experience = data.get("experience")
    work_type = data.get("work_type")
    employment_type = data.get("employment_type")
    company_logo = data.get("company_logo")
    url = data.get("url")
    company_name = data.get("company_name")
    addresses = data.get("addresses")

    existing_offer = JobOffer.objects.filter(url=url).exists()
    if not existing_offer:

        employment_type_objects = []
        if employment_type:
            for et in employment_type:
                employment_obj, created = EmploymentType.objects.get_or_create(name=et)
                employment_type_objects.append(employment_obj)
        work_type_objects = []
        if work_type:
            for wt in work_type:
                work_obj, created = WorkType.objects.get_or_create(name=wt)
                work_type_objects.append(work_obj)

        experience_objects = []
        if experience:
            for exp in experience:
                exp_obj, created = Experience.objects.get_or_create(name=exp)
                experience_objects.append(exp_obj)

        salary_objects = []
        if salaries:
            for salary in salaries:
                salary_from = salary.get("salary_from")
                salary_to = salary.get("salary_to")

                if not salary_from and not salary_to:
                    pass

                salary_objects.append(
                    Salary.objects.create(
                        salary_from=salary_from,
                        salary_to=salary_to,
                        currency=salary.get("currency"),
                        schedule=salary.get("schedule")
                    )
                )

        addresses_objects = []
        if addresses:
            for address in addresses:
                country = address.get("country")
                region = address.get("region")
                city = address.get("city")
                street = address.get("street")

                country_existing = Country.objects.filter(name=country).first() if country else None
                region_existing = Region.objects.filter(name=region).first() if region else None
                city_existing = City.objects.filter(name=city).first() if city else None

                country_obj, region_obj, city_obj = None, None, None

                if country_existing:
                    country_obj = country_existing
                else:
                    if country:
                        country_obj = Country.objects.create(name=country)

                if region_existing:
                    region_obj = region_existing
                    country_obj = region_existing.country
                else:
                    if region:
                        region_obj = Region.objects.create(name=region, country=country_obj)

                if city_existing:
                    city_obj = city_existing
                    region_obj = city_existing.region
                    country_obj = city_existing.country
                else:
                    if city:
                        city_obj = City.objects.create(
                            name=city,
                            region=region_obj,
                            country=country_obj
                        )

                address_obj, created = Address.objects.get_or_create(country=country_obj, region=region_obj,
                                                                     city=city_obj, street=street)

                addresses_objects.append(address_obj)

        offer = JobOffer.objects.create(
            title=title,
            description=description,
            is_remote=is_remote,
            is_hybrid=is_hybrid,
            skills=skills,
            company_logo=company_logo,
            company_name=company_name,
            url=url
        )

        offer.salary.add(*salary_objects)
        offer.work_type.add(*work_type_objects)
        offer.experience.add(*experience_objects)
        offer.employment_type.add(*employment_type_objects)
        offer.addresses.add(*addresses_objects)
