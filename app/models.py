from pydantic import BaseModel, EmailStr
from typing import Optional

# User model
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"  # Default role is "user"


# Category model
class Category(BaseModel):
    name: str

# Task model
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "Medium"
    user_id: Optional[int] = None
    category_id: Optional[int] = None