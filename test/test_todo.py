"""
in this file, we shall be creating a demo or a fake database
just for us to test the real functionality of our real database

"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from main import app
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todos


from routers.todos import get_db, get_current_user

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


def override_get_current_user():
    return {"username": "Benadfemtest", "id":1, "user_role": "admin"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

"""
we will need to create a fixture for the function and this is 
got from the pytest library that has been imported
"""
@pytest.fixture
def test_todos():
    todo = Todos(
        title="Learn to code!",
        description="Learn to code! Everyday",
        priority=5,
        completed=False,
        id = 1,
        owner_id = 1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()


def test_read_all_authenticated(test_todos):
    response = client.get("/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "title": "Learn to code!",
        "description": "Learn to code! Everyday",
        "priority": 5,
        "completed": False,
        "id": 1,
        "owner_id": 1
    }]