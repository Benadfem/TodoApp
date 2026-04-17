
from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated

from starlette import status

import models
from database import  SessionLocal
from models import Todos
from .auth import get_current_user


router = APIRouter()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# let's create a variable db_dependency to hold the annotation
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


"""
to create a new Todo we have to design the schema using the TodoRequest
"""
class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    completed: bool = Field(default=False)
    priority: int = Field(default=0, gt=0, lt=6)

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):
    return db.query(models.Todos).filter(Todos.owner_id == user.get('id')).all()


# getting a single info from the database
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_one(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail='Todo not found.')

"""
Now we will have to create a route the will enable the 
creation of new Todo in todos.db
"""
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,db: db_dependency, todo_request: TodoRequest ):
    if user is None:
        raise HTTPException(status_code=404, detail='Authentication failed ')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


"""
to Update a database
"""
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)
                      ):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise   HTTPException(status_code=404 ,detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.completed = todo_request.completed
    todo_model.priority = todo_request.priority

    db.add(todo_model)
    db.commit()

"""
    Personal ASSIGNMENT to get the list of todos with the same rating

"""

@router.get("/todo/priority/{todo_priority}", status_code=status.HTTP_200_OK)
async def read_todo_by_priority(db: db_dependency,
                                todo_priority: int = Path(gt=0, lt=6)):

    todo_model = db.query(Todos).filter(Todos.priority == todo_priority).all()

    if todo_model:
        return todo_model

    raise HTTPException(status_code=404, detail='No todos found with that priority.')

"""
We can decide to delete some data from the data base by todo_id
"""
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency ,todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()