from fastapi import APIRouter
from pydantic import BaseModel

from models import User

router = APIRouter()
class CreateUserRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    roles: str

@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = User(
       email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        roles=create_user_request.roles,
        hashed_password = create_user_request.password,
        is_active=True
    )
    return create_user_model