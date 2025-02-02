from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.postgres import get_async_session
from models.url import URL
from schemas.url import URLCreateRequest, URLCreateResponse
from utils.short_id import generate_short_id
from core.config import settings

router = APIRouter(prefix="/url", tags=["URL"])

@router.post("/create", summary="Create shorten version of URL")
async def create_shorten_url(request: URLCreateRequest, db: AsyncSession = Depends(get_async_session)) -> URLCreateResponse:
    """Создание сокращённого URL"""
    existing_url = await db.execute(select(URL).filter(URL.original_url == request.original_url))
    existing_url = existing_url.scalars().first()
    
    if existing_url:
        return URLCreateResponse(short_url=f"{settings.service_url}/{existing_url.short_id}")
    short_id = generate_short_id()
    
    new_url = URL(short_id=short_id, original_url=request.original_url, visibility=request.visibility)
    db.add(new_url)
    await db.commit()

    return URLCreateResponse(short_url=f"{settings.service_url}/{short_id}")