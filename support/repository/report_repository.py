from ..models import Report
from repository.crud import CRUDRepository


class ReportRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Report)
