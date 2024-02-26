from typing import Any, Optional, List, Dict
from rest_framework.exceptions import NotFound


class CRUDRepository:

    def __init__(self, model):
        self._model = model

    def get_all(self, user=None) -> List[Optional[Any]]:
        if user:
            return self._model.objects.filter(user=user).order_by('-created_at')
        else:
            return self._model.objects.all().order_by('-created_at')

    def get_by_id(self, _id: int, user=None) -> Optional[Any]:
        if not self.exists(_id):
            raise NotFound(f"Object with id {_id} does not exist")

        if user:
            return self._model.objects.get(id=_id, user=user)
        else:
            return self._model.objects.get(id=_id)

    def create(self, data) -> Any:
        return self._model.objects.create(**data)

    def update(self, _id: int, data: Dict, user=None) -> Optional[Any]:
        if not self.exists(_id, user):
            raise NotFound(f"Object with id {_id} does not exist")

        obj = self.get_by_id(_id, user)

        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
            return obj
        return None

    def delete(self, _id: int, user=None) -> None:
        if not self.exists(_id, user):
            raise NotFound(f"Object with id {_id} does not exist")
        obj = self.get_by_id(_id, user)
        if obj:
            obj.delete()
            return None
        return None

    def exists(self, _id: int, user=None) -> bool:
        if user:
            return self._model.objects.filter(id=_id, user=user).exists()
        else:
            return self._model.objects.filter(id=_id).exists()