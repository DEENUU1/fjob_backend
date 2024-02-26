from ..models import Salary
from repository.crud import CRUDRepository


class SalaryRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Salary)
