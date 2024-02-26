from ..models import Product
from repository.crud import CRUDRepository


class ProductRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Product)
