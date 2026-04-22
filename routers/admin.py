
from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated

from starlette import status

import models
from database import  SessionLocal
from models import Todos
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# let's create a variable db_dependency to hold the annotation
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/todos',status_code=status.HTTP_200_OK)
async def get_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Todos).all()
