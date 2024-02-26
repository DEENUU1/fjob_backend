from datetime import timedelta

from django.db.models import Count


class CandidateService:
    """
    Service class for handling operations related to Candidate entities.

    Attributes:
    - _repository: The repository used for database interactions.

    Methods:
    - __init__(self, repository): Initializes the CandidateService with a repository.
    - create(self, data): Creates a new candidate using the provided data.
    - count_candidate_status(self, job_offer_id: int): Counts the candidates' status for a specific job offer.
    - get_candidate_timeline(self, job_offer_id: int): Retrieves the timeline of candidate creation for a job offer.
    - get_user_applications(self, user): Retrieves the applications of a specific user.
    """

    def __init__(self, repository):
        """
        Initializes the CandidateService with a repository.

        Parameters:
        - repository: The repository used for database interactions.
        """
        self._repository = repository

    def create(self, data):
        """
        Creates a new candidate using the provided data.

        Parameters:
        - data: The data needed to create a new candidate.

        Returns:
        - Any: The result of the repository's create operation.
        """
        return self._repository.create(data)

    def count_candidate_status(self, job_offer_id: int):
        """
        Counts the candidates' status for a specific job offer.

        Parameters:
        - job_offer_id (int): The ID of the job offer.

        Returns:
        - dict: A dictionary containing counts for each candidate status (PENDING, ACCEPTED, REJECTED).
        """
        candidates = self._repository.filter_by_job_offer(job_offer_id)

        pending_count = candidates.filter(status="PENDING").count()
        accepted_count = candidates.filter(status="ACCEPTED").count()
        rejected_count = candidates.filter(status="REJECTED").count()
        all_objects = candidates.count()

        return {
            "count": all_objects,
            "pending": pending_count,
            "accepted": accepted_count,
            "rejected": rejected_count,
        }

    def get_candidate_timeline(self, job_offer_id: int):
        """
        Retrieves the timeline of candidate creation for a job offer.

        Parameters:
        - job_offer_id (int): The ID of the job offer.

        Returns:
        - list: A list of dictionaries containing dates and the corresponding number of candidates created.
        """
        candidates = self._repository.filter_by_job_offer(job_offer_id)

        num_candidates_per_day = (
            candidates
            .values('created_at__date')
            .annotate(num_candidates=Count('id'))
            .order_by('created_at__date')
        )

        start_date = num_candidates_per_day.first()['created_at__date']
        end_date = num_candidates_per_day.last()['created_at__date']
        all_dates = [
            start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)
        ]

        results_dict = {entry['created_at__date']: entry['num_candidates'] for entry in num_candidates_per_day}

        # Complete empty dates
        for date in all_dates:
            if date not in results_dict:
                results_dict[date] = 0

        # Sort data
        sorted_results = [
            {'created_at__date': str(date), 'num_candidates': results_dict[date]} for date in sorted(
                results_dict.keys()
            )
        ]
        return sorted_results

    def get_user_applications(self, user):
        """
        Retrieves the applications of a specific user.

        Parameters:
        - user: The user object.

        Returns:
        - QuerySet: A queryset containing applications filtered by the specified user.
        """
        return self._repository.filter_by_user(user)
