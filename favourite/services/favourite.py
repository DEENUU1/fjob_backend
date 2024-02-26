

class FavouriteService:
    def __init__(self, repository):
        self._repository = repository

    def get_all(self, user):
        return self._repository.get_all(user=user)

    def create(self, data):
        return self._repository.create(data)

    def delete(self, user, pk: int):
        return self._repository.delete(user=user, pk=pk)
