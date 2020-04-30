import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./db.sqlite3"

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, echo=False)
metadata = sqlalchemy.MetaData()
