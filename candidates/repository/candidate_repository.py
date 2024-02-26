from ..models import Candidate
from repository.crud import CRUDRepository


class CandidateRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Candidate)

    def filter_by_job_offer(self, _id: int):
        return self._model.objects.filter(job_offer_id=_id)

    def filter_by_user(self, user):
        return self._model.objects.filter(user=user)
