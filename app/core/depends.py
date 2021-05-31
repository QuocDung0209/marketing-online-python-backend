from typing import Generator

from app.db.session import SessionLocal


# Dependency to get DB session.
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
