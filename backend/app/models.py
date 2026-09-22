from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    applications = relationship("JobApplication", back_populates="owner", cascade="all, delete-orphan")

class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(150), nullable=False)
    position = Column(String(150), nullable=False)
    location = Column(String(150), default="")
    status = Column(String(50), default="Applied", index=True)
    job_url = Column(String(500), default="")
    applied_date = Column(Date, nullable=True)
    notes = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="applications")
