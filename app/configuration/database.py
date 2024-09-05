from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .settings import settings

engine = create_async_engine(settings.db_settings.db_url, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

sinc_engine = create_engine(settings.db_settings.db_url_sync, echo=True)
SyncSessionLocal = sessionmaker(bind=sinc_engine)