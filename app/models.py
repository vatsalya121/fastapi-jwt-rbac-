from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    role: str = Field(default="user")  # Roles: "user" or "admin"

    projects: List["Project"] = Relationship(back_populates="owner")


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    owner_id: int = Field(foreign_key="user.id")

    owner: User = Relationship(back_populates="projects")