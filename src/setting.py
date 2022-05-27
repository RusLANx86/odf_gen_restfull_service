"""Debug setting."""

from app.tools.setting import BaseConfig


class ProdConfig(BaseConfig):
    """Production configuration."""

    DB_URI = "postgresql+psycopg2://postgres:ghjcnjytnfr@192.168.128.251:5433/tmp"
    SWAGGER = {
        "swagger": "2.0",
        "info": {
            "title": "Шаблон",
            "description": "Проект шаблон.",
            "version": "1.0.0"
        },
        "schemes": [
            "http"
        ]
    }

class DevConfig(BaseConfig):
    """Development configuration."""

    DB_URI = "postgresql+psycopg2://postgres:ghjcnjytnfr@192.168.128.251:5433/tmp"
    SWAGGER = {
        "swagger": "2.0",
        "info": {
            "title": "Шаблон",
            "description": "Проект шаблон.",
            "version": "1.0.0"
        },
        "schemes": [
            "http"
        ]
    }