from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from .models import User, Project
from .schemas import UserCreate, UserLogin, ProjectCreate
from .auth import get_current_user, create_access_token, get_password_hash, verify_password
from .database import get_session, engine, create_db_and_tables

app = FastAPI(title="FastAPI JWT RBAC",
    description="A simple API with JWT authentication and role-based access control.",
    version="1.0.0",)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password, role=user.role)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/projects")
def read_projects(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return session.query(Project).all()

@app.post("/projects")
def create_project(project: ProjectCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    db_project = Project(name=project.name, description=project.description, owner_id=current_user.id)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@app.put("/projects/{project_id}")
def update_project(
    project_id: int,
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    db_project = session.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_project.name = project.name
    db_project.description = project.description
    session.commit()
    session.refresh(db_project)

    return db_project

@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    db_project = session.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    session.delete(db_project)
    session.commit()

    return {"message": "Project deleted successfully"}