from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from Intership_Recommendation_system.db.db_config import SessionLocal, engine
import Intership_Recommendation_system.db.db_model as db_model
from model import UserCreate, UserUpdate

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
db_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message": "Welcome to Internship Recommendation Engine 🚀"}


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========== USER ROUTES ==========

# Add new user (signup)
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db_model.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get all users
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(db_model.User).all()


# Get user by Clerk ID
@app.get("/users/{clerk_id}")
def get_user(clerk_id: str, db: Session = Depends(get_db)):
    user = db.query(db_model.User).filter(db_model.User.clerk_id == clerk_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


# Update user info (after signup)
@app.put("/users/{clerk_id}")
def update_user(clerk_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(db_model.User).filter(db_model.User.clerk_id == clerk_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# Delete user
@app.delete("/users/{clerk_id}")
def delete_user(clerk_id: str, db: Session = Depends(get_db)):
    db_user = db.query(db_model.User).filter(db_model.User.clerk_id == clerk_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": f"User with Clerk ID {clerk_id} deleted successfully"}


