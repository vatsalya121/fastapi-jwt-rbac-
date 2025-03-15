from sqlmodel import Session
from .models import User, Project

def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_username(session: Session, username: str):
    return session.query(User).filter(User.username == username).first()

def create_project(session: Session, project: Project):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

def get_projects(session: Session):
    return session.query(Project).all()