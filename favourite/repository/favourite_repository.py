from ..models import Favourite
from repository.crud import CRUDRepository


class FavouriteRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Favourite)
