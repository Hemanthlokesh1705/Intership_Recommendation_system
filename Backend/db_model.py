from sqlalchemy import Column, String, Integer, Date, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    # Clerk auth details
    clerk_id = Column(String(100), primary_key=True, index=True)
    name = Column(String(200))
    email = Column(String(200), unique=True, index=True)
    signup_time = Column(String(100))  # can store as string/timestamp

    # Personal details
    address = Column(Text, nullable=True)
    phone_number = Column(String(15), nullable=True)
    gender = Column(String(20), nullable=True)
    dob = Column(Date, nullable=True)

    # Academic details
    college_name = Column(String(200), nullable=True)
    semester = Column(Integer, nullable=True)
    branch = Column(String(100), nullable=True)
    graduation_year = Column(Integer, nullable=True)

    # Skills/Interests
    sector_interested = Column(String(200), nullable=True)
    skills = Column(Text, nullable=True)  # store as CSV string or JSON
    internship_type = Column(String(100), nullable=True)  # e.g., "Full-time", "Part-time"
    location_preference = Column(String(200), nullable=True)  # e.g., "Remote", "On-site"
    
