from pydantic import BaseModel

import uuid


class UserRole(BaseModel):
    id: str


class UserAccount(BaseModel):
    username: str
    password: str


class UserProfile(BaseModel):
    full_name: str
    e_mail: str

    
class User(BaseModel):
    account: UserAccount
    profile: UserProfile
    role: UserRole







class CreateUser(User):
    class Config:
        orm_mode = True

class DeleteUser(User):
    class Config:
        orm_mode = True

class UpdateUser(User):
    class Config:
        orm_mode = True




from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()

