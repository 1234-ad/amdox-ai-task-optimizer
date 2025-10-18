"""
Database Connection
Handles database connections and session management
"""

import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/amdox_task_optimizer')

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=os.getenv('SQL_ECHO', 'False').lower() == 'true'
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)

# Base class for models
Base = declarative_base()

def init_db():
    """Initialize database - create all tables"""
    try:
        from .models import Employee, Task, EmotionAnalysis, Alert
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        # For demo purposes, we'll continue even if DB is not available
        logger.warning("Continuing without database connection")

def get_db_session():
    """Get a database session"""
    return Session()

@contextmanager
def session_scope():
    """Provide a transactional scope for database operations"""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        session.close()

def close_db():
    """Close database connections"""
    Session.remove()
    engine.dispose()
    logger.info("Database connections closed")
