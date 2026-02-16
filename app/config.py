from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30
    environment: str = "development"

    model_config = {"env_file": ".env"}


settings = Settings()
