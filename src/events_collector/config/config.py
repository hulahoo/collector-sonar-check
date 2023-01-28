from pydantic import BaseSettings


class Settings(BaseSettings):

    KAFKA_BOOTSTRAP_SERVER: str = "kafka:9092"
    TOPIC_CONSUME_EVENTS: str = "syslog"
    KAFKA_GROUP_ID: str = "main"
    TOPIC_TO_EXPORT_EVENTS: str = "collector"
    CSRF_ENABLED: bool = True
    SESSION_COOKIE_SECURE: bool = True

    APP_POSTGRESQL_HOST: str = "localhost"
    APP_POSTGRESQL_PASSWORD: str = "password"
    APP_POSTGRESQL_USER: str = "username"
    APP_POSTGRESQL_NAME: str = "db"
    APP_POSTGRESQL_PORT: int = 5432

    class Config:
        env_file = "./.env"


settings = Settings()
