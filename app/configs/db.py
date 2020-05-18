DB_CONFIG = {
    "connections": {
        # "default": {
        #     "engine": "tortoise.backends.asyncpg",
        #     "credentials": {
        #         "host": "localhost",
        #         "port": "5432",
        #         "user": "tortoise",
        #         "password": "qwerty123",
        #         "database": "test",
        #     }
        # },
        "develop": "sqlite://db.sqlite3"
        # "develop": "sqlite://:memory:"
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "develop",
        }
    }
}
