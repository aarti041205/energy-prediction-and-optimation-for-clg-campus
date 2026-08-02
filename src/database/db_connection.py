"""
Database Connection and Session Management for PostgreSQL.
Provides SQLAlchemy engine, declarative base, session generator, and connection health verification.
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.config import DATABASE_URL
from src.utils.logger import logger

Base = declarative_base()

try:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 5}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("SQLAlchemy database engine initialized.")
except Exception as e:
    logger.warning(f"PostgreSQL connection initialization deferred or offline: {e}")
    # Fallback SQLite in-memory or sqlite file if postgresql is unavailable locally
    fallback_url = "sqlite:///./campus_energy_fallback.db"
    engine = create_engine(fallback_url, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Fallback SQLite database initialized.")

def get_db():
    """
    Dependency generator for FastAPI database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Creates all database tables defined in ORM models.
    """
    try:
        from src.database.models import PredictionRecord, AlertRecord, ChatRecord, ReportRecord, OptimizationLogRecord
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {e}")
        return False

def check_db_connection() -> bool:
    """
    Verifies live database connectivity.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        return False