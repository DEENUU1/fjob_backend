class CompanyService:
    """
    Service class for handling operations related to Company entities.

    Attributes:
    - _repository: The repository used for database interactions.

    Methods:
    - __init__(self, repository): Initializes the CompanyService with a repository.
    - get_all_active(self): Retrieves all active companies.
    - get_active_by_slug(self, slug: str): Retrieves an active company by its slug.
    - get_company_by_user(self, user): Retrieves a company by its associated user.
    - increment_num_of_available_offers(self, company_id: int, value: int): Increments the number of available offers
      for a company.
    """

    def __init__(self, repository):
        """
        Initializes the CompanyService with a repository.

        Parameters:
        - repository: The repository used for database interactions.
        """
        self._repository = repository

    def get_all_active(self):
        """
        Retrieves all active companies.

        Returns:
        - QuerySet: A queryset containing all active companies.
        """
        return self._repository.get_all_active()

    def get_active_by_slug(self, slug: str):
        """
        Retrieves an active company by its slug.

        Parameters:
        - slug (str): The slug of the company.

        Returns:
        - Company or None: The active company with the specified slug or None if not found.
        """
        return self._repository.get_active_by_slug(slug)

    def get_company_by_user(self, user):
        """
        Retrieves a company by its associated user.

        Parameters:
        - user: The user object associated with the company.

        Returns:
        - Company or None: The company associated with the specified user or None if not found.
        """
        return self._repository.get_company_by_user(user)

    def increment_num_of_available_offers(self, company_id: int, value: int):
        """
        Increments the number of available offers for a company.

        Parameters:
        - company_id (int): The ID of the company.
        - value (int): The value by which to increment the number of available offers.

        Returns:
        - None
        """
        return self._repository.increment_num_of_available_offers(company_id, value)
