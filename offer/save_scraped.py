from typing import Dict, Any

from location.models import City, Region, Country, Address
from offer.models import JobOffer, EmploymentType, WorkType, Experience, Salary


def save_scraped(data: Dict[str, Any]) -> None:
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
                employment_type_objects.append(EmploymentType.objects.get_or_create(name=et))

        work_type_objects = []
        if work_type:
            for wt in work_type:
                work_type_objects.append(WorkType.objects.get_or_create(name=wt))

        experience_objects = []
        if experience:
            for exp in experience:
                experience_objects.append(Experience.objects.get_or_create(name=exp))

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

                country_obj, region_obj, city_obj = None, None, None

                if country:
                    country_obj, created = Country.objects.get_or_create(name=country)

                if region:
                    region_obj, created = Region.objects.get_or_create(name=region, country=country_obj)

                if city:
                    city_obj, created = City.objects.get_or_create(name=city, region=region_obj,
                                                                   country=country_obj)

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
