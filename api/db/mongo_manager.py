import json
import os
import uuid
import typing as t

import bson
from bson.json_util import dumps
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from api.db.database_manager import DatabaseManager
from api.public.traffics.models import Traffic, TrafficUpdate
from api.utils.logger import logger_config

logger = logger_config(__name__)


class MongoManager(DatabaseManager):
    """
    This class extends from api./database_manager.py
    which have the abstract methods to be re-used here.
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    # database connect and close connections
    async def connect_to_database(self, path: str) -> None:
        logger.info("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)

        if os.getenv("ENVIRONMENT") == "PRD":
            self.db = self.client.users_prd
        elif os.getenv("ENVIRONMENT") == "STG":
            self.db = self.client.users_stg
        else:
            self.db = self.client.users_dev

        logger.info(
            "Connected to MongoDB -  %s environment!", os.getenv("ENVIRONMENT", "DEV")
        )

    async def close_database_connection(self) -> None:
        logger.info("Closing connection to MongoDB")
        self.client.close()
        logger.info("MongoDB connection closed")

    # to be used from /api/public endpoints
    async def entity_get_total(self) -> int:
        total: int = await self.db.traffics.count_documents({})
        return total

    async def entity_get_actives(self) -> int:
        traffics = self.db.traffics.find({"active": True})
        users_list = []
        async for traffic in traffics:
            users_list.append(json.loads(dumps(traffic)))

        return len(users_list)

    async def entity_get_all(self) -> t.List[Traffic]:
        users_list = []
        traffics = self.db.traffics.find()

        async for traffic in traffics:
            del traffic["_id"]
            users_list.append(json.loads(dumps(traffic)))

        return users_list

    async def entity_get_one(self, traffic_id: t.Union[str, bson.Binary]) -> Traffic:
        if isinstance(traffic_id, str):
            traffics = self.db.traffics.find({"traffic_id": bson.Binary.from_uuid(uuid.UUID(traffic_id))})
        else:
            traffics = self.db.traffics.find({"traffic_id": traffic_id})

        async for traffic in traffics:
            del traffic["_id"]
            return json.loads(dumps(traffic))

    async def entity_add_one(self, traffic: Traffic) -> Traffic:
        traffic_exist = await self.entity_get_one(traffic_id=traffic.dict()["traffic_id"])
        if traffic_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"traffic: {traffic_exist['traffic_id']} already exist",
            )

        await self.db.traffics.insert_one(traffic.dict())

        traffic = await self.entity_get_one(traffic_id=traffic.dict()["traffic_id"])

        return traffic

    async def entity_update_one(self, traffic_id: str, traffic: TrafficUpdate) -> Traffic:

        _traffic: dict = traffic.dict()
        bson_id: bson.Binary = bson.Binary.from_uuid(uuid.UUID(traffic_id))
        _traffic["traffic_id"] = bson_id
        await self.db.traffics.update_one({"traffic_id": _traffic["traffic_id"]}, {"$set": _traffic})
        traffic_updated = await self.entity_get_one(traffic_id=_traffic["traffic_id"])

        return traffic_updated

    async def entity_delete_one(self, traffic_id: t.Union[str, bson.Binary]) -> str:
        if isinstance(traffic_id, str):
            await self.db.traffics.delete_one({"traffic_id": bson.Binary.from_uuid(uuid.UUID(traffic_id))})
        else:
            await self.db.traffics.delete_one({"traffic_id": traffic_id})

        return json.dumps(f"__SUCCESS__")
