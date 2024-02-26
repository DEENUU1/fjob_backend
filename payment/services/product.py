

class ProductService:
    def __init__(self, repository):
        self._repository = repository

    def get_all(self):
        return self._repository.get_all()
