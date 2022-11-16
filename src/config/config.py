from pydantic import BaseSettings


class Settings(BaseSettings):

    KAFKA_BOOTSTRAP_SERVER: str = "localhost"
    TOPIC_CONSUME_EVENTS: str = ""
    KAFKA_GROUP_ID: str = "collector"

    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_DB_PORT: int = 5432
    POSTGRES_DB: str = "db"

    class Config:
        env_file = "./.env"


settings = Settings()
