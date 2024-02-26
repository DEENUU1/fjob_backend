from ..models import Company
from repository.crud import CRUDRepository


class CompanyRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Company)

    def get_all_active(self):
        return self._model.objects.filter(is_active=True)

    def get_active_by_slug(self, slug: str):
        return self._model.objects.filter(is_active=True, slug=slug).first()

    def get_company_by_user(self, user):
        return self._model.objects.filter(user=user).first()
