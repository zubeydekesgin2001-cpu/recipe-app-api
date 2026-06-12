from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class RecipeCreate(BaseModel):
    title: str
    description: str
    ingredients: str
    instructions: str
    category: str
    difficulty: str
    photo: str
    user_id: int


class RecipeResponse(BaseModel):
    id: int
    title: str
    description: str
    ingredients: str
    instructions: str
    category: str
    difficulty: str
    photo: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    value: int
    comment: str
    user_id: int
    recipe_id: int


class RatingResponse(BaseModel):
    id: int
    value: int
    comment: str
    user_id: int
    recipe_id: int
    created_at: datetime

    class Config:
        from_attributes = True