from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserRequest(BaseModel):
    username: str
    password: str
    phone: str

class UserAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role_level: int