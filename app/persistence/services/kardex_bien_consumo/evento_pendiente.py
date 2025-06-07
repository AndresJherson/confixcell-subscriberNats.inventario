from uuid import uuid4
from sqlmodel import col, select
from app.domain.dtos.WrapperKardexBienConsumoDTO import WrapperKardexBienConsumoDTO
from app.persistence.database.database import get_session_destino
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.orms.EventoPendienteKardexBienConsumoOrm import EventoPendienteKardexBienConsumoOrm
from app.persistence.orms.KardexBienConsumoOrm import KardexBienConsumoOrm

class EventoPendienteKardexBienConsumoService:
    
    @staticmethod
    async def guardar_evento_pendiente(evento: str, almacen_uuid: str, bien_consumo_uuid: str, wrapper: WrapperKardexBienConsumoDTO):
        async with get_session_destino() as session:
            result = await session.execute(
                select(KardexBienConsumoOrm)
                .where(
                    KardexBienConsumoOrm.almacen_uuid == almacen_uuid,
                    KardexBienConsumoOrm.bien_consumo_uuid == bien_consumo_uuid
                )
            )
            kardex = result.scalars().first()

            if kardex and kardex.id is not None:
                pendiente = EventoPendienteKardexBienConsumoOrm(
                    uuid=str(uuid4()),
                    kardex_bien_consumo_id=kardex.id,
                    evento=evento,
                    data=wrapper.model_dump()
                )
                session.add(pendiente)
                await session.commit()


    @staticmethod
    async def obtener_evento_pendiente(session: AsyncSession, almacen_uuid: str, bien_consumo_uuid: str):
        result = await session.execute(
            select(EventoPendienteKardexBienConsumoOrm)
            .join(KardexBienConsumoOrm)
            .where(
                KardexBienConsumoOrm.almacen_uuid == almacen_uuid,
                KardexBienConsumoOrm.bien_consumo_uuid == bien_consumo_uuid
            )
            .order_by(
                col(EventoPendienteKardexBienConsumoOrm.fecha).asc(),
                col(EventoPendienteKardexBienConsumoOrm.id).asc()
            )
        )
        kardex = result.scalars().first()
        return kardex