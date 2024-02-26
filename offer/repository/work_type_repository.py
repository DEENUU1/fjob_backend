from ..models import WorkType
from repository.crud import CRUDRepository


class WorkTypeRepository(CRUDRepository):
    def __init__(self):
        super().__init__(WorkType)
