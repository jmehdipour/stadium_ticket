from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class UserIn(BaseModel):
    password: str
    full_name: str
    email: str


class UserOut(BaseModel):
    id: int = Field(alias='_id')
    full_name: str
    email: str


class UserTypeEnums(Enum):
    normal = 1001
    admin = 1002


class SeatCategory(BaseModel):
    name: str
    number_of_seats: int


class StadiumIn(BaseModel):
    name: str
    city: str
    sales_participation: float
    seat_categories: List[SeatCategory] = []


class MatchIn(BaseModel):
    host_team: str
    guest_team: str
    stadium_id: int
    starts_at: datetime
    ends_at: datetime
