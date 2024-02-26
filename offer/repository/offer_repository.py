from typing import List

from location.models import City, Region, Country, Address
from offer.models import JobOffer, EmploymentType, WorkType, Experience, Salary
from repository.crud import CRUDRepository


class OfferRepository(CRUDRepository):
    """
    Repository class for CRUD operations on JobOffer model and related entities.

    Inherits from CRUDRepository.

    Methods:
    - __init__(self): Constructor to initialize the repository with the JobOffer model.
    - create_addresses(self, addresses) -> List[Address]: Creates Address objects based on provided data.
    - create_salary(self, salaries) -> List[Salary]: Creates Salary objects based on provided data.
    - create_employment_type(self, employment_type) -> List[EmploymentType]: Creates EmploymentType objects based on provided data.
    - create_work_type(self, work_type) -> List[WorkType]: Creates WorkType objects based on provided data.
    - create_experience(self, experience) -> List[Experience]: Creates Experience objects based on provided data.
    - create_offer(self, employment_type, work_type, experience, salaries, addresses, title, description, is_remote, is_hybrid, skills, company_logo, company_name, url) -> None: Creates a JobOffer object with related entities.
    - save_scraped(self, data: Dict[str, Any]) -> None: Saves scraped data into the database.

    Attributes:
    - None
    """

    def __init__(self):
        """
        Constructor to initialize the repository with the JobOffer model.
        """
        super().__init__(JobOffer)

    def create_addresses(self, addresses) -> List:
        """
        Creates Address objects based on provided data.

        Parameters:
        - addresses (List[Dict[str, str]]): List of address data.

        Returns:
        - List[Address]: List of created Address objects.
        """
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

        return addresses_objects

    def create_salary(self, salaries) -> List:
        """
        Creates Salary objects based on provided data.

        Parameters:
        - salaries (List[Dict[str, Any]]): List of salary data.

        Returns:
        - List[Salary]: List of created Salary objects.
        """
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
        return salary_objects

    def create_employment_type(self, employment_type) -> List:
        """
        Creates EmploymentType objects based on provided data.

        Parameters:
        - employment_type (List[str]): List of employment type names.

        Returns:
        - List[EmploymentType]: List of created EmploymentType objects.
        """
        employment_type_objects = []
        if employment_type:
            for et in employment_type:
                employment_obj, created = EmploymentType.objects.get_or_create(name=et)
                employment_type_objects.append(employment_obj)
        return employment_type_objects

    def create_work_type(self, work_type) -> List:
        """
        Creates WorkType objects based on provided data.

        Parameters:
        - work_type (List[str]): List of work type names.

        Returns:
        - List[WorkType]: List of created WorkType objects.
        """
        work_type_objects = []
        if work_type:
            for wt in work_type:
                work_obj, created = WorkType.objects.get_or_create(name=wt)
                work_type_objects.append(work_obj)
        return work_type_objects

    def create_experience(self, experience) -> List:
        """
        Creates Experience objects based on provided data.

        Parameters:
        - experience (List[str]): List of experience names.

        Returns:
        - List[Experience]: List of created Experience objects.
        """
        experience_objects = []
        if experience:
            for exp in experience:
                exp_obj, created = Experience.objects.get_or_create(name=exp)
                experience_objects.append(exp_obj)
        return experience_objects

    def create_offer(
            self,
            employment_type,
            work_type,
            experience,
            salaries,
            addresses,
            title,
            description,
            is_remote,
            is_hybrid,
            skills,
            company_logo,
            company_name,
            url
    ) -> None:
        """
        Creates a JobOffer object with related entities.

        Parameters:
        - employment_type (List[str]): List of employment type names.
        - work_type (List[str]): List of work type names.
        - experience (List[str]): List of experience names.
        - salaries (List[Dict[str, Any]]): List of salary data.
        - addresses (List[Dict[str, str]]): List of address data.
        - title (str): Job offer title.
        - description (str): Job offer description.
        - is_remote (bool): Whether the job offer is remote.
        - is_hybrid (bool): Whether the job offer is hybrid.
        - skills (str): Required skills for the job offer.
        - company_logo (str): URL of the company logo.
        - company_name (str): Name of the company.
        - url (str): URL of the job offer.

        Returns:
        - None
        """
        employment_type_objects = self.create_employment_type(employment_type)
        work_type_objects = self.create_work_type(work_type)
        experience_objects = self.create_experience(experience)
        salary_objects = self.create_salary(salaries)
        addresses_objects = self.create_addresses(addresses)

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

    def save_scraped(self, data: Dict[str, Any]) -> None:
        """
        Saves scraped data into the database.

        Parameters:
        - data (Dict[str, Any]): Scraped data.

        Returns:
        - None
        """
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
            self.create_offer(
                employment_type=employment_type,
                work_type=work_type,
                experience=experience,
                salaries=salaries,
                addresses=addresses,
                title=title,
                description=description,
                is_remote=is_remote,
                is_hybrid=is_hybrid,
                skills=skills,
                company_logo=company_logo,
                company_name=company_name,
                url=url,
            )
