from ..models import Favourite
from repository.crud import CRUDRepository


class FavouriteRepository(CRUDRepository):
    """
    Repository class for managing Favourite objects in a database.

    This class extends the CRUDRepository, providing basic CRUD operations for Favourite entities.

    Attributes:
    - _model (Favourite): The model class for Favourite entities.

    Methods:
    - __init__(self): Initializes the FavouriteRepository, setting the model class.
    """

    def __init__(self):
        """
        Initializes the FavouriteRepository with the Favourite model.
        """
        super().__init__(Favourite)
