"""
Database configuration and session management for the Travel Planner backend.

This module sets up SQLAlchemy engine, session handling, and base declarative class.
It reads the database URL from the environment variable TRAVEL_PLANNER_DB_URL and
falls back to a local SQLite database file when not provided.

Environment:
    TRAVEL_PLANNER_DB_URL: Optional. SQLAlchemy-style database URL. Example:
        - sqlite:///./travel_planner.db (default)
        - sqlite:////data/travel_planner.db
        - postgresql+psycopg2://user:password@host:5432/dbname

Notes:
    - We intentionally do not create a separate DB container. Persistence is within this backend container.
"""
from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Read DB URL from env with a sensible default to local SQLite file in container working dir
DEFAULT_SQLITE_URL = "sqlite:///./travel_planner.db"
DATABASE_URL = os.getenv("TRAVEL_PLANNER_DB_URL", DEFAULT_SQLITE_URL)

# For SQLite, need check_same_thread=False for usage with FastAPI (multi-threaded)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Create engine and session factory
engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session, future=True)

# Base declarative class for models
Base = declarative_base()


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Provide a SQLAlchemy session dependency for FastAPI routes and services.

    Yields:
        Session: A database session bound to the configured engine. Closes after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PUBLIC_INTERFACE
def init_db() -> None:
    """Initialize the database by creating all tables if they do not exist."""
    from src.api.models import Base as ModelsBase  # Ensure models are imported and registered
    ModelsBase.metadata.create_all(bind=engine)
