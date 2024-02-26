from repository.crud import CRUDRepository
from ..models import Company


class CompanyRepository(CRUDRepository):
    """
    Repository class for managing Company objects in a database.

    This class extends the CRUDRepository, providing basic CRUD operations for Company entities.

    Attributes:
    - _model (Company): The model class for Company entities.

    Methods:
    - __init__(self): Initializes the CompanyRepository, setting the model class.
    - get_all_active(self): Retrieves all active companies.
    - get_active_by_slug(self, slug: str): Retrieves an active company by its slug.
    - get_company_by_user(self, user): Retrieves a company by its associated user.
    - increment_num_of_available_offers(self, company_id: int, value: int): Increments the number of available offers for a company.
    """

    def __init__(self):
        """
        Initializes the CompanyRepository with the Company model.
        """
        super().__init__(Company)

    def get_all_active(self):
        """
        Retrieves all active companies.

        Returns:
        - QuerySet: A queryset containing all active companies.
        """
        return self._model.objects.filter(is_active=True)

    def get_active_by_slug(self, slug: str):
        """
        Retrieves an active company by its slug.

        Parameters:
        - slug (str): The slug of the company.

        Returns:
        - Company or None: The active company with the specified slug or None if not found.
        """
        return self._model.objects.filter(is_active=True, slug=slug).first()

    def get_company_by_user(self, user):
        """
        Retrieves a company by its associated user.

        Parameters:
        - user: The user object associated with the company.

        Returns:
        - Company or None: The company associated with the specified user or None if not found.
        """
        return self._model.objects.filter(user=user).first()

    def increment_num_of_available_offers(self, company_id: int, value: int):
        """
        Increments the number of available offers for a company.

        Parameters:
        - company_id (int): The ID of the company.
        - value (int): The value by which to increment the number of available offers.
        """
        company = self.get_by_id(company_id)
        company.num_of_available_offers += value
        company.save()
