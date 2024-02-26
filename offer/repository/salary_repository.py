from repository.crud import CRUDRepository
from ..models import Salary


class SalaryRepository(CRUDRepository):
    """
    Repository class for CRUD operations on Salary model.

    Inherits from CRUDRepository.

    Methods:
    - __init__(self): Constructor to initialize the repository with the Salary model.

    Attributes:
    - None
    """

    def __init__(self):
        """
        Constructor to initialize the repository with the Salary model.
        """
        super().__init__(Salary)
