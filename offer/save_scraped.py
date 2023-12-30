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
            for address_data in addresses:
                country_name = address_data.get("country")
                region_name = address_data.get("region")
                city_name = address_data.get("city")
                street = address_data.get("street")

                city_obj, created_city = City.objects.get_or_create(name=city_name)

                if not created_city:
                    region_obj = city_obj.region
                    country_obj = city_obj.country
                else:
                    region_obj, country_obj = None, None

                region_obj, created_region = Region.objects.get_or_create(name=region_name, country=country_obj)

                if not created_region:
                    country_obj = region_obj.country
                else:
                    country_obj = None

                country_obj, created_country = Country.objects.get_or_create(name=country_name)

                address_obj, created = Address.objects.get_or_create(
                    country=country_obj,
                    region=region_obj,
                    city=city_obj,
                    street=street
                )

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
