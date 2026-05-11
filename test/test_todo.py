"""
in this file, we shall be creating a demo or a fake database
just for us to test the real functionality of our real database

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from main import app


from routers.todos import get_db

# this creates a new database though it is fake compared to the production database
SQLALCHEMY_DATABASE_URI = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool
                       )


TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False,bind=engine)

Base.metadata.create_all(engine)

# this creates a function to override the get_db in the database file.
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db