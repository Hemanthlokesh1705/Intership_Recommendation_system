from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    clerk_id: str
    name: str
    email: str
    signup_time: str

    # Optional details
    address: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None

    college_name: Optional[str] = None
    semester: Optional[int] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None

    sector_interested: Optional[str] = None
    skills: Optional[str] = None
    interested_field: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    address: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    college_name: Optional[str] = None
    semester: Optional[int] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    sector_interested: Optional[str] = None
    skills: Optional[str] = None
    interested_field: Optional[str] = None
