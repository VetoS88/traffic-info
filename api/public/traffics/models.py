import typing as t
import datetime
import uuid
import bson
from pydantic import BaseModel, Field
from dataclasses import dataclass


@dataclass(frozen=True)
class TrafficDirection:
    """
    Направления проезда транспортного средства
    """
    ENTRY: str = "__ENTRY__"
    EXIT: str = "__EXIT__"


@dataclass(frozen=True)
class TrafficTypes:
    """
    Типы транспортных средств
    """
    LIGHT_VEHICLE: str = "__LIGHT_VEHICLE__"
    CARGO_VEHICLE: str = "__CARGO_VEHICLE__"


def default_uuid_factory() -> bson.Binary:
    """
    Функция генерации уникального uuid, конвертированного в bson
    """
    return bson.Binary.from_uuid(uuid.uuid4())


class Traffic(BaseModel):
    """
    Модель информации о проезде транспортного средства
    """
    traffic_id: bson.Binary = Field(default_factory=default_uuid_factory, alias="_id")
    time: datetime.datetime = Field(default_factory=datetime.datetime.now)
    traffic_num: str = Field()
    direction: str = Field()
    traffic_type: str = Field()
    image_url: str = Field()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "traffic_num": "х999км",
                "direction": TrafficDirection.ENTRY,
                "traffic_type": TrafficTypes.LIGHT_VEHICLE,
                "image_url": ""
            }
        }


class TrafficUpdate(BaseModel):
    time: t.Optional[datetime.datetime]
    traffic_num: t.Optional[str]
    direction: t.Optional[str]
    traffic_type: t.Optional[str]
    image_url: t.Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "time": "2021-09-02 15:32:15",
                "traffic_num": "х997км",
                "direction": TrafficDirection.EXIT,
                "traffic_type": TrafficTypes.CARGO_VEHICLE,
                "image_url": ""
            }
        }
