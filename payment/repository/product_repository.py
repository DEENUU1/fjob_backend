from repository.crud import CRUDRepository
from ..models import Product


class ProductRepository(CRUDRepository):
    """
    Repository class for managing Product objects in a database.

    This class extends the CRUDRepository, providing basic CRUD operations for Product entities.

    Attributes:
    - _model (Product): The model class for Product entities.

    Methods:
    - __init__(self): Initializes the ProductRepository, setting the model class.
    """

    def __init__(self):
        """
        Initializes the ProductRepository with the Product model.
        """
        super().__init__(Product)
