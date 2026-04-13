from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

import models
from database import SessionLocal
from models import Users

router = APIRouter()

# This Secret and algorithm for the authorization of user in the application
SECRET_KEY = 'a750047dfaae5e3969e4d6d3be17348fe90525b2406924e330445e5cacba7ce1'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    roles: str


"""
create a class Token 
"""
class Token(BaseModel):
    access_token: str
    token_type: str

"""
We need to add this user to the database 
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# let's create a variable db_dependency to hold the annotation
db_dependency = Annotated[Session, Depends(get_db)]

# let's create an authentication entry for the user
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id :int, expires_delta:timedelta):
    encode ={'sub': username, 'id': user_id}
    expires = (datetime.now(timezone.utc)+ expires_delta)
    # encode.update({'exp': expires})
    encode.update({'exp': int(expires.timestamp())})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
       email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        roles=create_user_request.roles,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()

@router.get("/auth/user")
async def get_user(db: db_dependency):
    return db.query(models.Users).all()

""" 
We have to create the access token for each user.
"""
@router.post("/token", response_model=Token,status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        # Better than returning a string; this sends a real error response
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user."
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
