import uvicorn
import logging

from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.logger import LOGGING
from core.config import settings


app = FastAPI(
    title=settings.project_name,
    default_response_class=ORJSONResponse,
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/docs.json",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.service_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )