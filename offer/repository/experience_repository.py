from ..models import Experience
from repository.crud import CRUDRepository


class ExperienceRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Experience)
