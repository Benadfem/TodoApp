

from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated

from starlette import status

import models
from database import engine, SessionLocal
from models import Todos

app = FastAPI()

"""
fastapi will automatically create a database for the applicaiton 
since there is model an database connection creation 
"""
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# let's create a variable db_dependency to hold the annotation
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(models.Todos).all()


# getting a single info from the database
@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_one(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail='Todo not found.')
