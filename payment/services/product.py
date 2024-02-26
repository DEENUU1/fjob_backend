class ProductService:
    """
    Service class for handling operations related to Product entities.

    Attributes:
    - _repository: The repository used for database interactions.

    Methods:
    - __init__(self, repository): Initializes the ProductService with a repository.
    - get_all(self): Retrieves all products.

    """

    def __init__(self, repository):
        """
        Initializes the ProductService with a repository.

        Parameters:
        - repository: The repository used for database interactions.
        """
        self._repository = repository

    def get_all(self):
        """
        Retrieves all products.

        Returns:
        - QuerySet: A queryset containing all products.
        """
        return self._repository.get_all()
