from ..models import WorkType
from repository.crud import CRUDRepository


class WorkTypeRepository(CRUDRepository):
    """
    Repository class for CRUD operations on WorkType model.

    Inherits from CRUDRepository.

    Methods:
    - __init__(self): Constructor to initialize the repository with the WorkType model.

    Attributes:
    - None
    """

    def __init__(self):
        """
        Constructor to initialize the repository with the WorkType model.
        """
        super().__init__(WorkType)
