from typing import Generator, Any
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
import settings
from main import app
import os
import asyncio
from db.session import get_db
import asyncpg


test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)

test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

CLEAN_TABLES = [
    "users",
]

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")

@pytest.fixture(scope="session", autouse=True)
async def async_session_test():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session

@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(f"""TRUNCATE TABLE {table_for_cleaning};""")

