
class ContactService:
    """
    Service class for handling operations related to Contact entities.

    Attributes:
    - _repository: The repository used for database interactions.

    Methods:
    - __init__(self, repository): Initializes the ContactService with a repository.
    - create(self, data): Creates a new Contact entity with the provided data.
    """

    def __init__(self, repository):
        """
        Initializes the ContactService with a repository.

        Parameters:
        - repository: The repository used for database interactions.
        """
        self._repository = repository

    def create(self, data):
        """
        Creates a new Contact entity with the provided data.

        Parameters:
        - data: The data to create the Contact entity.

        Returns:
        - Any: The created Contact entity.
        """
        return self._repository.create(data)
