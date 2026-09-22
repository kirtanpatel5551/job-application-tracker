from datetime import date, datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ApplicationBase(BaseModel):
    company: str
    position: str
    location: str = ""
    status: str = "Applied"
    job_url: str = ""
    applied_date: date | None = None
    notes: str = ""

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(ApplicationBase):
    pass

class ApplicationOut(ApplicationBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DashboardOut(BaseModel):
    total: int
    applied: int
    interview: int
    offer: int
    rejected: int
