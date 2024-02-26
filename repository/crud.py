from typing import Any, Optional, List, Dict

from rest_framework.exceptions import NotFound


class CRUDRepository:
    """
    Generic repository class for basic CRUD operations on a model.

    Attributes:
    - _model: The model class for the repository.

    Methods:
    - __init__(self, model): Initializes the CRUDRepository with the provided model.
    - get_all(self, user=None) -> List[Optional[Any]]: Retrieves all objects, optionally filtered by user.
    - get_by_id(self, _id: int, user=None) -> Optional[Any]: Retrieves an object by its ID, optionally filtered by user.
    - create(self, data) -> Any: Creates a new object with the provided data.
    - update(self, _id: int, data: Dict, user=None) -> Optional[Any]: Updates an existing object by its ID, optionally filtered by user.
    - delete(self, _id: int, user=None) -> None: Deletes an object by its ID, optionally filtered by user.
    - exists(self, _id: int, user=None) -> bool: Checks if an object with the given ID exists, optionally filtered by user.
    """

    def __init__(self, model):
        """
        Initializes the CRUDRepository with the provided model.

        Parameters:
        - model: The model class for the repository.
        """
        self._model = model

    def get_all(self, user=None) -> List[Optional[Any]]:
        """
        Retrieves all objects, optionally filtered by user.

        Parameters:
        - user: The user object (default is None).

        Returns:
        - List[Optional[Any]]: A list of objects.
        """
        if user:
            return self._model.objects.filter(user=user).order_by('-created_at')
        else:
            return self._model.objects.all().order_by('-created_at')

    def get_by_id(self, _id: int, user=None) -> Optional[Any]:
        """
        Retrieves an object by its ID, optionally filtered by user.

        Parameters:
        - _id: The ID of the object.
        - user: The user object (default is None).

        Returns:
        - Optional[Any]: The retrieved object or None.
        """
        if not self.exists(_id):
            raise NotFound(f"Object with id {_id} does not exist")

        if user:
            return self._model.objects.get(id=_id, user=user)
        else:
            return self._model.objects.get(id=_id)

    def create(self, data) -> Any:
        """
        Creates a new object with the provided data.

        Parameters:
        - data: The data to create the object.

        Returns:
        - Any: The created object.
        """
        return self._model.objects.create(**data)

    def update(self, _id: int, data: Dict, user=None) -> Optional[Any]:
        """
        Updates an existing object by its ID, optionally filtered by user.

        Parameters:
        - _id: The ID of the object to update.
        - data: The data to update the object.
        - user: The user object (default is None).

        Returns:
        - Optional[Any]: The updated object or None.
        """
        if not self.exists(_id, user):
            raise NotFound(f"Object with id {_id} does not exist")

        obj = self.get_by_id(_id, user)

        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
            return obj
        return None

    def delete(self, _id: int, user=None) -> None:
        """
        Deletes an object by its ID, optionally filtered by user.

        Parameters:
        - _id: The ID of the object to delete.
        - user: The user object (default is None).

        Returns:
        - None
        """
        if not self.exists(_id, user):
            raise NotFound(f"Object with id {_id} does not exist")
        obj = self.get_by_id(_id, user)
        if obj:
            obj.delete()
            return None
        return None

    def exists(self, _id: int, user=None) -> bool:
        """
        Checks if an object with the given ID exists, optionally filtered by user.

        Parameters:
        - _id: The ID of the object to check.
        - user: The user object (default is None).

        Returns:
        - bool: True if the object exists, False otherwise.
        """
        if user:
            return self._model.objects.filter(id=_id, user=user).exists()
        else:
            return self._model.objects.filter(id=_id).exists()
