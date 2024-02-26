

class CompanyService:
    def __init__(self, repository):
        self._repository = repository

    def get_all_active(self):
        return self._repository.get_all_active()

    def get_active_by_slug(self, slug: str):
        return self._repository.get_active_by_slug(slug)

    def get_company_by_user(self, user):
        return self._repository.get_company_by_user(user)

    def increment_num_of_available_offers(self, company_id: int, value: int):
        return self._repository.increment_num_of_available_offers(company_id, value)