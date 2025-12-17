from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Klasa dostępu do zmiennych środowiskowych
    """
    DATABASE_URL: str

settings = Settings()