from typing import Any
from sqlmodel import col, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.entities import EventoPendienteKardexBienConsumoEntity, KardexBienConsumoEntity

async def guardar_evento_kardex_pendiente(session: AsyncSession, evento: str, almacen_uuid: str, bien_consumo_uuid: str, data: dict[Any, Any]):
    result = await session.execute(
        select(KardexBienConsumoEntity)
        .where(
            KardexBienConsumoEntity.almacen_uuid == almacen_uuid,
            KardexBienConsumoEntity.bien_consumo_uuid == bien_consumo_uuid
        )
    )
    kardex = result.scalars().first()

    if kardex and kardex.id is not None:
        pendiente = EventoPendienteKardexBienConsumoEntity(
            kardex_bien_consumo_id=kardex.id,
            evento=evento,
            data=data
        )
        session.add(pendiente)
        await session.commit()


async def obtener_evento_kardex_pendiente(session: AsyncSession, almacen_uuid: str, bien_consumo_uuid: str):
    result = await session.execute(
        select(EventoPendienteKardexBienConsumoEntity)
        .join(KardexBienConsumoEntity)
        .where(
            KardexBienConsumoEntity.almacen_uuid == almacen_uuid,
            KardexBienConsumoEntity.bien_consumo_uuid == bien_consumo_uuid
        )
        .order_by(
            col(EventoPendienteKardexBienConsumoEntity.fecha).asc(),
            col(EventoPendienteKardexBienConsumoEntity.id).asc()
        )
    )
    kardex = result.scalars().first()
    return kardex