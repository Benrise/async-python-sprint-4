import os

from logging import config as logging_config
from core.logger import LOGGING
from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging_config.dictConfig(LOGGING)

class Settings(BaseSettings):
    project_name: str = Field(..., alias="BACKEND_PROJECT_NAME")
    service_host: str = Field(..., alias="BACKEND_HOST")
    service_port: int = Field(..., alias="BACKEND_PORT")
    is_debug: bool = Field(..., alias="BACKEND_DEBUG")
    
settings = Settings()

class PostgresSettings(BaseSettings):
    db: str = Field(..., alias='DB_NAME')
    user: str = Field(..., alias='DB_USER')
    password: str = Field(..., alias='DB_PASSWORD')
    host: str = Field(..., alias='DB_HOST')
    port: int = Field(..., alias='DB_PORT')


pg = PostgresSettings()