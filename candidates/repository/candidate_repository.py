from repository.crud import CRUDRepository
from ..models import Candidate


class CandidateRepository(CRUDRepository):
    """
    Repository class for managing Candidate objects in a database.

    This class extends the CRUDRepository, providing basic CRUD operations for Candidate entities.

    Attributes:
    - _model (Candidate): The model class for Candidate entities.

    Methods:
    - __init__(self): Initializes the CandidateRepository, setting the model class.
    - filter_by_job_offer(self, _id: int): Filters candidates by job offer ID.
    - filter_by_user(self, user): Filters candidates by user.
    """

    def __init__(self):
        """
        Initializes the CandidateRepository with the Candidate model.
        """
        super().__init__(Candidate)

    def filter_by_job_offer(self, _id: int):
        """
        Filters candidates by job offer ID.

        Parameters:
        - _id (int): The ID of the job offer to filter candidates by.

        Returns:
        - QuerySet: A queryset containing candidates filtered by the specified job offer ID.
        """
        return self._model.objects.filter(job_offer_id=_id)

    def filter_by_user(self, user):
        """
        Filters candidates by user.

        Parameters:
        - user: The user object to filter candidates by.

        Returns:
        - QuerySet: A queryset containing candidates filtered by the specified user.
        """
        return self._model.objects.filter(user=user)
