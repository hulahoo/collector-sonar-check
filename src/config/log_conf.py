import sys

# TODO: подумать над форматом сообщения
fmt = "{time} | {level} | {name}:{function}:{line} -> {message}"


conf = {
    "handlers": [
        {"sink": sys.stdout, "format": fmt},
    ]
}
