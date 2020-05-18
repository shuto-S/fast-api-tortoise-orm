from os import environ


DB_CONFIG = {
    "connections": {
        # "production": {
        #     "engine": "tortoise.backends.asyncpg",
        #     "credentials": {
        #         "host": environ.get("DB_HOST", "localhost"),
        #         "port": environ.get("DB_PORT", "3306"),
        #         "user": environ.get("DB_USER", "root"),
        #         "password": environ.get("DB_PASSWORD", "root"),
        #         "database": environ.get("DB_DATABASE", "sample"),
        #     }
        # },
        "development": "sqlite://db.sqlite3",
        "test": "sqlite://:memory:"
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": environ.get("ENV", "development"),
        }
    }
}
