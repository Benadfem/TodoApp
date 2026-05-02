
from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.orm import Session
from typing import Annotated

from starlette import status

import models
from database import  SessionLocal
from models import Todos,Users
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/user',
    tags=['user']
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
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    # Using 'id' here to match your updated auth payload
    return db.query(Users).filter(Users.id == user.get('id')).first()

