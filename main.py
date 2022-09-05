import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics


from api.config import get_config
from api.db import db
from api.utils.logger import logger_config

from api.config import default_route
from api.public.traffics.views import router

logger = logger_config(__name__)

settings = get_config()
app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"{default_route}/swagger",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# prometheus metrics: https://prometheus.io/
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)
app.include_router(router)

logger.info(
    "FastAPI Mongo Async API has been launched for %s environment!",
    settings.ENVIRONMENT,
)


@app.on_event("startup")
async def startup() -> None:
    """
    Создание клиента MongoDB при инициализации сервиса
    """
    logger.info("db connection startup")
    await db.connect_to_database(path=settings.DB_URI)
    traffics_list = await db.entity_get_all()
    if traffics_list is None or len(traffics_list) == 0:
        traffic_sample = Traffic(
            traffic_num="х999км",
            direction="__ENTRY__",
            traffic_type="__LIGHT_VEHICLE__",
            image_url="")
        await db.entity_add_one(traffic=traffic_sample)


@app.on_event("shutdown")
async def shutdown() -> None:
    """
    Отключение клиента MongoDB при отключении сервиса
    """
    logger.info("db connection startup")
    await db.close_database_connection()


def main() -> None:
    uvicorn.run(app, host='0.0.0.0', port=4666, debug=False)


if __name__ == '__main__':
    main()

