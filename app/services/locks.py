from datetime import datetime, timezone
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.entities import KardexLockEntity


async def intentar_bloquear_clave(session: AsyncSession, clave: str) -> bool:
    result = await session.execute(
        select(KardexLockEntity).where(KardexLockEntity.clave == clave)
    )
    existe = result.scalars().first()
    
    if existe:
        return False

    session.add(KardexLockEntity(
        clave=clave,
        fecha=datetime.now(timezone.utc)
    ))
    await session.commit()
    return True


async def liberar_clave(session: AsyncSession, clave: str):
    result = await session.execute(
        select(KardexLockEntity).where(KardexLockEntity.clave == clave)
    )
    lock = result.scalars().first()
    
    if lock:
        await session.delete(lock)
        await session.commit()
