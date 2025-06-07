from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import DB_DESTINO_HOST, DB_DESTINO_NAME, DB_DESTINO_PASSWORD, DB_DESTINO_USER, DB_ORIGEN_HOST, DB_ORIGEN_NAME, DB_ORIGEN_PASSWORD, DB_ORIGEN_USER

_connection_origen = f"mysql+aiomysql://{DB_ORIGEN_USER}:{DB_ORIGEN_PASSWORD}@{DB_ORIGEN_HOST}/{DB_ORIGEN_NAME}"
_engine_origen = create_async_engine(_connection_origen)
_async_session_origen = async_sessionmaker(
    bind=_engine_origen,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_session_origen():
    async with _async_session_origen() as session:
        await session.execute(text("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ"))
        yield session
    

_connection_destino = f"mysql+aiomysql://{DB_DESTINO_USER}:{DB_DESTINO_PASSWORD}@{DB_DESTINO_HOST}/{DB_DESTINO_NAME}"
engine_destino = create_async_engine(_connection_destino)
_async_session_destino = async_sessionmaker(
    bind=engine_destino,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_session_destino():
    async with _async_session_destino() as session:
        await session.execute(text("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED"))
        yield session