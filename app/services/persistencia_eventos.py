from typing import Any
from sqlmodel import Session, col, select
from app.entities import EventoPendienteKardexBienConsumoEntity, KardexBienConsumoEntity

async def guardar_evento_kardex_pendiente(session: Session, evento: str, almacen_uuid: str, bien_consumo_uuid: str, data: dict[Any, Any]):
    kardex = session.exec(
        select(KardexBienConsumoEntity)
        .where(
            KardexBienConsumoEntity.almacen_uuid == almacen_uuid,
            KardexBienConsumoEntity.bien_consumo_uuid == bien_consumo_uuid
        )
    ).first()

    if kardex and kardex.id is not None:
        pendiente = EventoPendienteKardexBienConsumoEntity(
            kardex_bien_consumo_id=kardex.id,
            evento=evento,
            data=data
        )
        session.add(pendiente)
        session.commit()


def obtener_evento_kardex_pendiente(session: Session, almacen_uuid: str, bien_consumo_uuid: str):
    evento_pendiente = session.exec(
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
    ).first()
    
    return evento_pendiente