from repository.crud import CRUDRepository
from ..models import PaymentInfo


class PaymentInfoRepository(CRUDRepository):
    """
    Repository class for managing PaymentInfo objects in a database.

    This class extends the CRUDRepository, providing basic CRUD operations for PaymentInfo entities.

    Attributes:
    - _model (PaymentInfo): The model class for PaymentInfo entities.

    Methods:
    - __init__(self): Initializes the PaymentInfoRepository, setting the model class.
    """

    def __init__(self):
        """
        Initializes the PaymentInfoRepository with the PaymentInfo model.
        """
        super().__init__(PaymentInfo)
