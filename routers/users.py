
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

class PhoneNumberVerification(BaseModel):
    phone_number: str
    new_phone_number: str = Field(min_length=11, max_length=11)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    # Using 'id' here to match your updated auth payload
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/phone_number', status_code=status.HTTP_200_OK)
def update_phone_number(user: user_dependency, db: db_dependency, phone_verification: PhoneNumberVerification):
    if user is None:
        raise HTTPException(status_code=204, detail='Phone number not found!')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not phone_verification.phone_number and user_model.phone_number:
        raise HTTPException(status_code=401, detail='Error on Phone number change')

    user_model.phone_number= phone_verification.new_phone_number
    db.add(user_model)
    db.commit()

    return "Phone number updated successfully!"

@router.put('/password', status_code=status.HTTP_201_CREATED)
def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()