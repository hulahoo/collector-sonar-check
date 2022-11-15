from typing import List, Tuple

from pydantic import BaseSettings


class Settings(BaseSettings):

    EMAIL_FROM: str = "FEMA"
    EMAIL_SUBJECT: str = "SEMA"
    MD5_HASH: str = "MD5H"
    SHA1_HASH: str = "SHA1"
    SHA256_HASH: str = "SHA2"
    IP: str = "IPAD"
    URL: str = "URLS"
    DOMAIN: str = "DOMN"
    FILENAME: str = "FILE"
    REGISTRY: str = "REGS"

    TYPE_OF_INDICATOR_CHOICES: List[Tuple[str, str]] = [
        (EMAIL_FROM, "Email's origin"),
        (EMAIL_SUBJECT, "Email's subject"),
        (MD5_HASH, "File hashe MD5"),
        (SHA1_HASH, "File hashe SHA1"),
        (SHA256_HASH, "File hashe SHA256"),
        (FILENAME, "File name"),
        (REGISTRY, "Registry"),
        (IP, "IP adresses"),
        (URL, "Full URL's"),
        (DOMAIN, "Domain's"),
    ]

    KAFKA_BOOTSTRAP_SERVER: str = "localhost"
    TOPIC_CONSUME_EVENTS: str = ""
    KAFKA_GROUP_ID: str = "collector"

    class Config:
        env_prefix = "COLLECTOR_"
        env_file = "./.env"


settings = Settings()
