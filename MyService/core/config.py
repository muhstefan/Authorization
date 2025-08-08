from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_echo: bool = False
    db_url: str

    class Config:
        env_file = ".env"


settings = Settings()  # Создаем объект класса выше
