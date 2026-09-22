from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import Base, engine, get_db
from .models import User, JobApplication
from .schemas import UserCreate, UserOut, Token, ApplicationCreate, ApplicationUpdate, ApplicationOut, DashboardOut
from .auth import hash_password, verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Job Application Tracker API", "docs": "/docs"}

@app.post("/auth/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/auth/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return Token(access_token=create_access_token(user.id))

@app.get("/api/applications", response_model=list[ApplicationOut])
def list_applications(
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = db.query(JobApplication).filter(JobApplication.owner_id == user.id)
    if status:
        query = query.filter(func.lower(JobApplication.status) == status.lower())
    return query.order_by(JobApplication.created_at.desc()).all()

@app.post("/api/applications", response_model=ApplicationOut, status_code=201)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = JobApplication(**payload.model_dump(), owner_id=user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/api/applications/{application_id}", response_model=ApplicationOut)
def get_application(application_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.owner_id == user.id,
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Application not found")
    return item

@app.put("/api/applications/{application_id}", response_model=ApplicationOut)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.owner_id == user.id,
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Application not found")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@app.delete("/api/applications/{application_id}", status_code=204)
def delete_application(application_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.owner_id == user.id,
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(item)
    db.commit()

@app.get("/api/dashboard", response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    statuses = [row[0] for row in db.query(JobApplication.status).filter(JobApplication.owner_id == user.id).all()]
    lowered = [s.lower() for s in statuses]
    return DashboardOut(
        total=len(statuses),
        applied=lowered.count("applied"),
        interview=lowered.count("interview"),
        offer=lowered.count("offer"),
        rejected=lowered.count("rejected"),
    )
