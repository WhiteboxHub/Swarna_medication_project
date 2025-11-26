from motor.motor_asyncio import AsyncIOMotorClient
from app.db.repository import Repository
from typing import Dict, Any, Optional, List
from uuid import uuid4
from datetime import datetime


class DocumentDBRepository(Repository):
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def create(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        data = data.copy()
        data["id"] = data.get("id", str(uuid4()))
        data["created_at"] = data.get("created_at", datetime.utcnow())

        await self.db[collection].insert_one(data)
        return data

    async def get_by_id(
        self, collection: str, id: str
    ) -> Optional[Dict[str, Any]]:
        doc = await self.db[collection].find_one(
            {"id": id},
            {"_id": 0}   # ✅ Remove Mongo internal _id
        )
        return doc

    async def find(
        self, collection: str, filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        cursor = self.db[collection].find(
            filters,
            {"_id": 0}
        )
        return await cursor.to_list(length=None)

    async def update(
        self,
        collection: str,
        id: str,
        update_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        result = await self.db[collection].update_one(
            {"id": id},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError(f"{collection} id {id} not found")

        return await self.get_by_id(collection, id)
