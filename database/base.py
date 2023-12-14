from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine('postgresql+asyncpg://postgres:1234@127.0.0.1:5433/qwqw', echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
