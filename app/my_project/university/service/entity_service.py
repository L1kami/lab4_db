from typing import Any


class EntityService:
    def __init__(self, dao, dto_type):
        self.dao = dao
        self.dto_type = dto_type

    def get_all(self):
        return [self.dto_type(**item).to_dict() for item in self.dao.find_all()]

    def get_by_id(self, item_id):
        item = self.dao.find_by_id(item_id)
        return self.dto_type(**item).to_dict() if item else None

    def create(self, data: dict[str, Any]):
        return self.dao.create(data)

    def update(self, item_id, data: dict[str, Any]):
        return self.dao.update(item_id, data)

    def delete(self, item_id):
        return self.dao.delete(item_id)
