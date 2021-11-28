from pydantic import BaseModel, Field


class UserIn(BaseModel):
    password: str
    full_name: str
    email: str


class UserOut(BaseModel):
    id: int = Field(alias='_id')
    full_name: str
    email: str
