import uvicorn
import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.postgres import get_async_session
from models.url import URL, URLAccess
from core.logger import LOGGING
from core.config import settings
from api.v1 import health
from api.v1 import url
from middlewares.blocked_ip import BlockedIPMiddleware


app = FastAPI(
    title=settings.project_name,
    default_response_class=ORJSONResponse,
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/docs.json",
)

app.include_router(health.router)
app.include_router(url.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BlockedIPMiddleware, blocked_ips=settings.blocked_ips)

@app.get("/{short_id}", summary="Get original URL and redirect")
async def get_original_url(short_id: str, request: Request, db: AsyncSession = Depends(get_async_session)):
    url = await db.execute(select(URL).filter(URL.short_id == short_id))
    url = url.scalars().first()
    
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if url.is_deleted:
        raise HTTPException(status_code=410, detail="URL is deleted")
    
    client_info = {
        "user_agent": request.headers.get("User-Agent"),
        "ip": request.client.host,
        "referer": request.headers.get("Referer"),
        "accept_language": request.headers.get("Accept-Language"),
    }
    
    new_access = URLAccess(url_id=url.id, client_info=str(client_info))
    db.add(new_access)
    await db.commit()
    
    return RedirectResponse(url.original_url, status_code=307)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.service_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )