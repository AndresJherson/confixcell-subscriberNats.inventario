from datetime import datetime, timezone
from uuid import uuid4
from sqlmodel import select

from app.persistence.database.database import get_session_destino
from app.persistence.orms.KardexLockOrm import KardexLockOrm

class KardexLockService:
    
    @staticmethod
    async def intentar_bloquear_clave(clave: str) -> bool:
        async with get_session_destino() as session:
            result = await session.execute(
                select(KardexLockOrm).where(KardexLockOrm.clave == clave)
            )
            existe = result.scalars().first()
            
            if existe:
                return False

            session.add(KardexLockOrm(
                uuid=str(uuid4()),
                clave=clave,
                fecha=datetime.now(timezone.utc)
            ))
            await session.commit()
            return True


    @staticmethod
    async def liberar_clave(clave: str):
        async with get_session_destino() as session:
            result = await session.execute(
                select(KardexLockOrm).where(KardexLockOrm.clave == clave)
            )
            lock = result.scalars().first()
            
            if lock:
                await session.delete(lock)
                await session.commit()
