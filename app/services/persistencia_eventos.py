from typing import Any
from sqlmodel import Session, col, select

from app.entities import EventoPendienteKardexBienConsumoEntity, KardexBienConsumoEntity

async def guardar_evento_kardex_pendiente(session: Session, evento: str, almacen_uuid: str, bien_consumo_uuid: str, data: dict[Any, Any]):
    kardex = session.exec(
        select(KardexBienConsumoEntity).where(
            KardexBienConsumoEntity.almacen_uuid == almacen_uuid,
            KardexBienConsumoEntity.bien_consumo_uuid == bien_consumo_uuid
        )
    ).first()

    if kardex:
        data_id = session.exec(
            select(EventoPendienteKardexBienConsumoEntity).order_by(col(EventoPendienteKardexBienConsumoEntity.id).desc())
        ).first()
        
        pendiente = EventoPendienteKardexBienConsumoEntity(
            id=1 if data_id is None else data_id.id + 1,
            kardex_bien_consumo_id=kardex.id,
            evento=evento,
            data=data
        )
        session.add(pendiente)
        session.commit()
