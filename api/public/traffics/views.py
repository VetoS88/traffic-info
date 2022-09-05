import typing as t
import uuid

import bson
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from api.db import DatabaseManager, get_database
from api.models.generic import Error
from api.public.traffics.models import Traffic, TrafficUpdate
from api.utils.logger import logger_config
from api.config import default_route

logger = logger_config(__name__)

router = APIRouter()


@router.get(
    "/get-traffics",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": t.List[Traffic]},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": Error},
    },
)
async def get_all_traffics(db: DatabaseManager = Depends(get_database)) -> JSONResponse:
    """Возвращает список всех проездов транспортных средств"""
    traffics = await db.entity_get_all()
    if traffics:
        return JSONResponse(status_code=status.HTTP_200_OK, content=traffics)
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="database not ready"
    )


@router.get(
    "/get-traffics/{traffic_id}",
    responses={
        status.HTTP_200_OK: {"model": Traffic},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
async def get_traffic_by_id(traffic_id: str, db: DatabaseManager = Depends(get_database)) -> JSONResponse:
    """Возвращает информацию о проезде транспортного средства по заданному id"""
    traffic = await db.entity_get_one(traffic_id=traffic_id)

    if traffic:
        return JSONResponse(status_code=status.HTTP_200_OK, content=traffic)

    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"no user found with traffic_id: {traffic_id}",
    )


@router.post(
    "/insert-traffic",
    responses={
        status.HTTP_201_CREATED: {"model": Traffic},
        status.HTTP_409_CONFLICT: {"model": Error},
    },
)
async def insert_traffic(payload: Traffic, db: DatabaseManager = Depends(get_database)) -> JSONResponse:
    """
    Добавляет информацию о проезде транспортного средства
    """
    traffic_created = await db.entity_add_one(traffic=payload)

    if traffic_created:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=traffic_created)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"user could not be created",
    )


@router.patch(
    "/update-traffic/{id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": Traffic},
        status.HTTP_409_CONFLICT: {"model": Error},
    },
)
async def update_traffic(traffic_id: str, payload: TrafficUpdate, db: DatabaseManager = Depends(get_database)) -> JSONResponse:
    """
    Обновляет информацию о проезде транспортного средства по заданному id
    """
    traffic_updated = await db.entity_update_one(traffic=payload, traffic_id=traffic_id)

    if traffic_updated:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=traffic_updated)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="user could not be updated",
    )


@router.delete(
    "/delete-traffic/{id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": Traffic},
        status.HTTP_409_CONFLICT: {"model": Error},
    },
)
async def delete_traffic(traffic_id: str, db: DatabaseManager = Depends(get_database)) -> JSONResponse:
    """
    Удаляет информацию о проезде транспортного средства по заданному id
    """
    traffic_deleted = await db.entity_delete_one(traffic_id=traffic_id)

    if traffic_deleted:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=[])

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"user could not be deleted",
    )
