class ReportService:
    """
    Service class for handling operations related to Report entities.

    Attributes:
    - _repository: The repository used for database interactions.

    Methods:
    - __init__(self, repository): Initializes the ReportService with a repository.
    - create(self, data): Creates a new Report entity with the provided data.
    """

    def __init__(self, repository):
        """
        Initializes the ReportService with a repository.

        Parameters:
        - repository: The repository used for database interactions.
        """
        self._repository = repository

    def create(self, data):
        """
        Creates a new Report entity with the provided data.

        Parameters:
        - data: The data to create the Report entity.

        Returns:
        - Any: The created Report entity.
        """
        return self._repository.create(data)
