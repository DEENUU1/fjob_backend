from ..models import EmploymentType
from repository.crud import CRUDRepository


class EmploymentTypeRepository(CRUDRepository):
    """
    Repository class for CRUD operations on EmploymentType model.

    Inherits from CRUDRepository.

    Methods:
    - __init__(self): Constructor to initialize the repository with the EmploymentType model.

    Attributes:
    - None
    """

    def __init__(self):
        """
        Constructor to initialize the repository with the EmploymentType model.
        """
        super().__init__(EmploymentType)
