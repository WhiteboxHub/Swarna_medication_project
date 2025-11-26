from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime


class Repository(ABC):
    @abstractmethod
    async def create(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_by_id(
        self, collection: str, id: str
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def find(
        self, collection: str, filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def update(
        self,
        collection: str,
        id: str,
        update_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        pass


class InMemoryRepository(Repository):
    """
    Used for:
    - Local development
    - Unit testing
    - When USE_LOCAL_STORE=1
    """

    def __init__(self):
        self.store: Dict[str, Dict[str, Dict[str, Any]]] = {
            "medications": {},
            "schedules": {},
            "doses": {},
        }

    async def create(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        data = data.copy()
        data["id"] = data.get("id", str(uuid4()))
        data["created_at"] = data.get("created_at", datetime.utcnow())

        self.store[collection][data["id"]] = data
        return data

    async def get_by_id(
        self, collection: str, id: str
    ) -> Optional[Dict[str, Any]]:
        return self.store[collection].get(id)
    
    # async def get_schedule_by_id(self,collection : str , id: str):

    #     data = self.store[collection]
    #     print(data)
    #     for d in data:
    #         if d['id'] == id:
    #             return d
    #     return None


    async def find(
        self, collection: str, filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        results = []
        for item in self.store[collection].values():
            if all(item.get(k) == v for k, v in filters.items()):
                results.append(item)
        return results

    async def update(
        self,
        collection: str,
        id: str,
        update_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        if id not in self.store[collection]:
            raise ValueError(f"{collection} with id {id} not found")

        self.store[collection][id].update(update_data)
        return self.store[collection][id]
