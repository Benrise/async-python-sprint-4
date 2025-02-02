from pydantic import BaseModel

from models.enums import VisibilityEnum


class URLCreateRequest(BaseModel):
    original_url: str = "http://example.com"
    visibility: VisibilityEnum = VisibilityEnum.public
    
class URLCreateResponse(BaseModel):
    short_url: str