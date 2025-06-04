from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    active = "active"
    completed = "completed"
    in_progress = "in_progress"
    on_hold = "on_hold"
    archived = "archived"
    planning = "planning"


class ProjectCategory(str, Enum):
    web_app = "web_app"
    mobile_app = "mobile_app"
    desktop_app = "desktop_app"
    api = "api"
    data_science = "data_science"
    machine_learning = "machine_learning"
    iot = "iot"
    game = "game"
    devops = "devops"
    other = "other"


class Technology(BaseModel):
    name: str
    version: Optional[str] = None
    category: str  # frontend, backend, database, etc.


class ProjectLink(BaseModel):
    title: str
    url: HttpUrl
    type: str  # github, demo, documentation, etc.


class ProjectContent(BaseModel):
    overview: str
    features: List[str]
    technical_details: str
    challenges: Optional[str] = None
    learnings: Optional[str] = None
    next_steps: Optional[str] = None


class Project(BaseModel):
    id: str = Field(..., description="Unique project identifier")
    title: str = Field(..., min_length=1, max_length=100)
    short_description: str = Field(..., min_length=1, max_length=200)
    category: ProjectCategory
    status: ProjectStatus
    technologies: List[Technology]
    links: List[ProjectLink] = []
    content: ProjectContent
    image_url: Optional[HttpUrl] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = []
    priority: int = Field(default=0, ge=0, le=10)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ProjectSummary(BaseModel):
    """Lightweight project model for menu/list views"""
    id: str
    title: str
    short_description: str
    category: ProjectCategory
    status: ProjectStatus
    image_url: Optional[HttpUrl] = None
    tags: List[str] = []
    priority: int


class ProjectsResponse(BaseModel):
    projects: List[ProjectSummary]
    total: int
    categories: Dict[str, int]  # category -> count


class ProjectFilter(BaseModel):
    category: Optional[ProjectCategory] = None
    status: Optional[ProjectStatus] = None
    tags: List[str] = []
    search: Optional[str] = None


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None 