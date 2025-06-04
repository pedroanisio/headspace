import os
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from typing import Generator

# Database URL from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://headspace_user:headspace_password@localhost:5432/headspace"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


class ProjectDB(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    short_description = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    technologies = Column(JSON, nullable=False, default=list)
    links = Column(JSON, nullable=False, default=list)
    content = Column(JSON, nullable=False)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(JSON, nullable=False, default=list)
    priority = Column(Integer, default=0)


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)


def init_db():
    """Initialize database with tables"""
    create_tables() 