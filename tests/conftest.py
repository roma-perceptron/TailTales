import sys
import pytest
from backend.db import engine, AsyncSession


def pytest_assertion_pass(item, lineno, orig, expl):
    sys.stdout.write(f"\n[ASSERT PASSED] В тесте {item.name} на строке {lineno}: {expl}\n")
    sys.stdout.flush()


@pytest.fixture
async def db_session():
    """На каждый тест своя сессия; scope="module" не поможет, да и не нужно уже"""
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            async with AsyncSession(bind=connection, expire_on_commit=False) as session:
                yield session
            #
            await transaction.rollback()
