from ..models import EmploymentType
from repository.crud import CRUDRepository


class EmploymentTypeRepository(CRUDRepository):
    def __init__(self):
        super().__init__(EmploymentType)
