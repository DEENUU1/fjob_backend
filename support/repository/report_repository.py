from repository.crud import CRUDRepository
from ..models import Report


class ReportRepository(CRUDRepository):
    """
    Repository class for managing Report objects in a database.

    This class extends the CRUDRepository, providing basic CRUD operations for Report entities.

    Attributes:
    - _model (Report): The model class for Report entities.

    Methods:
    - __init__(self): Initializes the ReportRepository, setting the model class.
    """

    def __init__(self):
        """
        Initializes the ReportRepository with the Report model.
        """
        super().__init__(Report)
