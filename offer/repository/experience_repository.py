from ..models import Experience
from repository.crud import CRUDRepository


class ExperienceRepository(CRUDRepository):
    """
    Repository class for CRUD operations on Experience model.

    Inherits from CRUDRepository.

    Methods:
    - __init__(self): Constructor to initialize the repository with the Experience model.

    Attributes:
    - None
    """

    def __init__(self):
        """
        Constructor to initialize the repository with the Experience model.
        """
        super().__init__(Experience)
