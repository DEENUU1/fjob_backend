class FavouriteService:
    """
    Service class for handling operations related to Favourite entities.

    Attributes:
    - _repository: The repository used for database interactions.

    Methods:
    - __init__(self, repository): Initializes the FavouriteService with a repository.
    - get_all(self, user): Retrieves all favourites for a specific user.
    - create(self, data): Creates a new favourite using the provided data.
    - delete(self, user, pk: int): Deletes a favourite for a specific user by its primary key.
    """

    def __init__(self, repository):
        """
        Initializes the FavouriteService with a repository.

        Parameters:
        - repository: The repository used for database interactions.
        """
        self._repository = repository

    def get_all(self, user):
        """
        Retrieves all favourites for a specific user.

        Parameters:
        - user: The user object.

        Returns:
        - QuerySet: A queryset containing all favourites for the specified user.
        """
        return self._repository.get_all(user=user)

    def create(self, data):
        """
        Creates a new favourite using the provided data.

        Parameters:
        - data: The data needed to create a new favourite.

        Returns:
        - Any: The result of the repository's create operation.
        """
        return self._repository.create(data)

    def delete(self, user, pk: int):
        """
        Deletes a favourite for a specific user by its primary key.

        Parameters:
        - user: The user object.
        - pk (int): The primary key of the favourite to be deleted.

        Returns:
        - None
        """
        return self._repository.delete(user=user, pk=pk)
