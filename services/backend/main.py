import uvicorn
import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.logger import LOGGING
from core.config import settings

from api.v1 import health
from api.v1 import url

app = FastAPI(
    title=settings.project_name,
    default_response_class=ORJSONResponse,
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/docs.json",
)

app.include_router(health.router)
app.include_router(url.router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.service_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )