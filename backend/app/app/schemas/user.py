from typing import Optional

from pydantic import BaseModel, EmailStr

__all__ = ["User", "UserCreate", "UserInDB", "UserUpdate"]


class UserBase(BaseModel):
    is_active: Optional[bool] = True
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    pass


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[int] = None
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass
