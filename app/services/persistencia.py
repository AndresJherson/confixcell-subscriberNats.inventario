from datetime import datetime, timezone
from dateutil import parser
from typing import Any
from sqlalchemy import delete, func, update
from sqlmodel import col, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.entities import EventoPendienteKardexBienConsumoEntity, KardexBienConsumoEntity, KardexMovimientoBienConsumoEntity

# EVENTOS
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


# KARDEX
async def crear_obtener_kardex(session: AsyncSession, almacen_uuid: str, bien_consumo_uuid: str) -> KardexBienConsumoEntity:
    
    result = await session.execute(
        select(KardexBienConsumoEntity).where(
            KardexBienConsumoEntity.almacen_uuid == almacen_uuid,
            KardexBienConsumoEntity.bien_consumo_uuid == bien_consumo_uuid
        )
    )
    kardex = result.scalars().first()

    if kardex is None:
        kardex = KardexBienConsumoEntity(
            almacen_uuid=almacen_uuid,
            bien_consumo_uuid=bien_consumo_uuid
        )
        session.add(kardex)
        await session.commit()
        await session.refresh(kardex)
    
    return kardex


# MOVIMIENTOS
async def crear_movimientos(session: AsyncSession, kardex_id: int, movimientos: list[dict[str, Any]]):
    if not movimientos:
        return None
    
    movimientos_ordenados = sorted(movimientos, key=lambda x: x["fecha"])
    session.add_all(KardexMovimientoBienConsumoEntity(
        kardex_bien_consumo_id=kardex_id,
        movimiento_uuid=mov["movimientosUuid"],
        movimiento_ref_uuid=mov["movimientoRefUuid"],
        movimiento_tipo=mov["movimientoTipo"],
        fecha=mov["fecha"],
        documento_fuente_cod_serie=mov["documentoFuenteCodigoSerie"],
        documento_fuente_cod_numero=mov["documentoFuenteCodigoNumero"],
        concepto=mov["concepto"],
        entrada_cant=mov["entradaCantidad"],
        entrada_costo_uni=mov["entradaCostoUnitario"],
        entrada_costo_tot=mov["entradaCostoTotal"],
        salida_cant=mov["salidaCantidad"],
        salida_costo_uni=mov["salidaCostoUnitario"],
        salida_costo_tot=mov["salidaCostoTotal"]
    ) for mov in movimientos_ordenados)
    await session.commit()
    
    return movimientos_ordenados[0]["fecha"]

async def actualizar_movimientos_by_id(session: AsyncSession, movimientos: list[dict[str, Any]]):
    fechas: list[Any] = []
    for mov in movimientos:
        if "fecha" in mov:
            fechas.append(mov["fecha"])
            
        await session.execute(
            update(KardexMovimientoBienConsumoEntity)
            .where(KardexMovimientoBienConsumoEntity.id == mov["id"])
            .values({k: v for k, v in mov.items() if k != "id"})
        )
        
    await session.commit()
    return min(fechas) if fechas else None


async def eliminar_movimientos_by_uuids(session: AsyncSession, movimientos: list[dict[str, Any]]):
    uuids = list(map(lambda x: str(x["movimientoUuid"]), movimientos))
    
    result = await session.execute(
        select(func.min(KardexMovimientoBienConsumoEntity.fecha))
        .where(col(KardexMovimientoBienConsumoEntity.movimiento_uuid).in_(uuids))
    )
    fecha = result.scalars().first()
    
    await session.execute(
        delete(KardexMovimientoBienConsumoEntity)
        .where(col(KardexMovimientoBienConsumoEntity.movimiento_uuid).in_(uuids))
    )
    await session.commit()
    
    return fecha


# FECHA
def to_utc_datetime(dt_raw: Any) -> datetime:
    if isinstance(dt_raw, str):
        dt = parser.isoparse(dt_raw)
    elif isinstance(dt_raw, datetime):
        dt = dt_raw
    else:
        raise ValueError(f"Fecha inválida: {dt_raw}")
                    
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt