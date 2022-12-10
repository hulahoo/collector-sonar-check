from enum import Enum


class TypesEnum(Enum):
    EMAIL_FROM: str = "FEMA"
    EMAIL_SUBJECT: str = "SEMA"
    MD5_HASH: str = "MD5H"
    SHA1_HASH: str = "SHA1"
    SHA256_HASH: str = "SHA2"
    IP: str = "IP"
    URL: str = "URL"
    DOMAIN: str = "DOMAIN"
    FILENAME: str = "FILE"
    REGISTRY: str = "REGISTRY"


TYPE_LIST = [type_ for type_ in dir(TypesEnum) if not type_.startswith('_')]
