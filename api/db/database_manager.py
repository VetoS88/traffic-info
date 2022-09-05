import typing as t
from abc import abstractmethod
from typing import List
import bson

from api.public.traffics.models import Traffic, TrafficUpdate


class DatabaseManager:
    """
    This class is meant to be extended from
    ./mongo_manager.py which will be the actual connection to mongodb.
    """

    @property
    def client(self) -> None:
        raise NotImplementedError

    @property
    def db(self) -> None:
        raise NotImplementedError

    # database connect and close connections
    @abstractmethod
    async def connect_to_database(self, path: str) -> None:
        pass

    @abstractmethod
    async def close_database_connection(self) -> None:
        pass

    # to be used from /api/public endpoints
    @abstractmethod
    async def entity_get_total(self) -> int:
        pass

    @abstractmethod
    async def entity_get_actives(self) -> int:
        pass

    @abstractmethod
    async def entity_get_all(self) -> List[Traffic]:
        pass

    @abstractmethod
    async def entity_get_one(self, traffic_id: str) -> List[Traffic]:
        pass

    @abstractmethod
    async def entity_add_one(self, traffic: Traffic) -> List[Traffic]:
        pass

    @abstractmethod
    async def entity_update_one(self, traffic_id: str, traffic: TrafficUpdate) -> Traffic:
        pass

    @abstractmethod
    async def entity_delete_one(self, traffic_id: t.Union[str, bson.Binary]) -> str:
        pass
