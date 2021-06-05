from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Synchronous database
# engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
# async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous Configuration
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
