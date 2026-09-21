from backend.config import DB_URL_ASYNC
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool


# базовый класс
class Base(DeclarativeBase):
    pass

# engine = create_async_engine(DB_URL_ASYNC, echo=False, pool_size=10, max_overflow=20, pool_recycle=60)
engine = create_async_engine(DB_URL_ASYNC, echo=True, poolclass=NullPool) # с новым соединением каждый раз
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session_maker() as session:
        yield session
