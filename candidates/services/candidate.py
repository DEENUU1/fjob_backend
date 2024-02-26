from datetime import timedelta

from django.db.models import Count


class CandidateService:

    def __init__(self, repository):
        self._repository = repository

    def create(self, data):
        return self._repository.create(data)

    def count_candidate_status(self, job_offer_id: int):
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
        candidates = self._repository.filter_by_job_offer(job_offer_id)

        num_candidates_per_day = candidates.values('created_at__date').annotate(num_candidates=Count('id')).order_by(
            'created_at__date')

        start_date = num_candidates_per_day.first()['created_at__date']
        end_date = num_candidates_per_day.last()['created_at__date']
        all_dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        results_dict = {entry['created_at__date']: entry['num_candidates'] for entry in num_candidates_per_day}

        # Complete empty dates
        for date in all_dates:
            if date not in results_dict:
                results_dict[date] = 0

        # Sort data
        sorted_results = [{'created_at__date': str(date), 'num_candidates': results_dict[date]} for date in
                          sorted(results_dict.keys())]
        return sorted_results

    def get_user_applications(self, user):
        return self._repository.filter_by_user(user)
