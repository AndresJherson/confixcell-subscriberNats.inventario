from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.persistence.orms.KardexBienConsumoOrm import KardexBienConsumoOrm

class KardexBienConsumoService:
    
    @staticmethod
    async def crear_obtener_kardex(session: AsyncSession, almacen_uuid: str, bien_consumo_uuid: str) -> KardexBienConsumoOrm:
        
        result = await session.execute(
            select(KardexBienConsumoOrm).where(
                KardexBienConsumoOrm.almacen_uuid == almacen_uuid,
                KardexBienConsumoOrm.bien_consumo_uuid == bien_consumo_uuid
            )
        )
        kardex = result.scalars().first()

        if kardex is None:
            kardex = KardexBienConsumoOrm(
                uuid=str(uuid4()),
                almacen_uuid=almacen_uuid,
                bien_consumo_uuid=bien_consumo_uuid
            )
            session.add(kardex)
            await session.commit()
            await session.refresh(kardex)
        
        return kardex


    @staticmethod
    async def obtener_kardex(session: AsyncSession, id: int):
        result = await session.execute(
            select(KardexBienConsumoOrm).where(
                KardexBienConsumoOrm.id == id,
            )
        )
        kardex = result.scalars().first()
        return kardex