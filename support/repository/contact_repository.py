from ..models import Contact
from repository.crud import CRUDRepository


class ContactRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Contact)
