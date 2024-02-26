from repository.crud import CRUDRepository
from ..models import Contact


class ContactRepository(CRUDRepository):
    """
    Repository class for managing Contact objects in a database.

    This class extends the CRUDRepository, providing basic CRUD operations for Contact entities.

    Attributes:
    - _model (Contact): The model class for Contact entities.

    Methods:
    - __init__(self): Initializes the ContactRepository, setting the model class.
    """

    def __init__(self):
        """
        Initializes the ContactRepository with the Contact model.
        """
        super().__init__(Contact)
