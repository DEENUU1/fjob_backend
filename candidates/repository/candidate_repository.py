from ..models import Candidate
from repository.crud import CRUDRepository


class CandidateRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Candidate)
