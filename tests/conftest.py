import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.cinema import Base
from app.main import app
from app.utils.depends import get_db

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False)

# Fixture to provide a database session for tests
@pytest.fixture(scope="function")
async def db_session():
    # Create tables before running the test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a session for the test
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        await session.close()
        # Drop tables after the tests are done
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

# Override the get_db dependency to use the test session
@pytest.fixture(scope="function", autouse=True)
def override_get_db(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides[get_db] = get_db

# Fixture for the FastAPI test client
@pytest.fixture(scope="module")
def test_app():
    from fastapi.testclient import TestClient
    client = TestClient(app)
    yield client
