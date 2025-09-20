from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., example="alice")
    salary: float = Field(default=0.0, ge=0, example=5000.0)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    user_id: int

    class Config:
        orm_mode = True
