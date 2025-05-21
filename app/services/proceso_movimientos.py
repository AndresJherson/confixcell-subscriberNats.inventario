from typing import Any, cast
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import KardexMovimientoBienConsumoEntity
from app.entities.KardexBienConsumoEntity import KardexBienConsumoEntity
from app.models.TipoEventosNats import EventoKardexBienConsumo


async def procesar_movimientos_por_evento(session: AsyncSession, evento: str, clave: str, almacen_uuid: str, bien_consumo_uuid: str, data: dict[str, Any]):
    match evento:
        
        case EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value:
            movimientos: list[dict[str, Any]] = data.get("crear", []).get(clave, []).get("movimientos", [])
            kardex = await _crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
            await _crear_movimientos(session, cast(int, kardex.id), movimientos )
            
        case EventoKardexBienConsumo.ACTUALIZAR_MOVIMIENTOS.value:
            movimientos_eliminar: list[dict[str, Any]] = data.get("eliminar", []).get(clave, []).get("movimientos", [])
            movimientos_crear: list[dict[str, Any]] = data.get("crear", []).get(clave, []).get("movimientos", [])
            kardex = await _crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
            await _actualizar_movimientos(session, cast(int, kardex.id), movimientos_eliminar, movimientos_crear)
                
        case EventoKardexBienConsumo.ELIMINAR_MOVIMIENTOS.value:
            movimientos: list[dict[str, Any]] = data.get("eliminar", []).get(clave, []).get("movimientos", [])
            kardex = await _crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
            await _eliminar_movimientos(session, cast(int, kardex.id), movimientos)
            
        case _:
            return None
        

async def _crear_obtener_kardex(session: AsyncSession, almacen_uuid: str, bien_consumo_uuid: str) -> KardexBienConsumoEntity:
    
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
    

async def _crear_movimientos(session: AsyncSession, kardex_id: int, movimientos: list[dict[str,Any]]):
    session.add_all(
        KardexMovimientoBienConsumoEntity(
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
            salida_costo_tot=mov["salidaCostoTotal"],
        ) for mov in movimientos
    )
    pass

async def _actualizar_movimientos(session: AsyncSession, kardex_id: int, movimientos_eliminar: list[dict[str,Any]], movimientos_crear: list[dict[str,Any]]):
    pass

async def _eliminar_movimientos(session: AsyncSession, kardex_id: int, movimientos: list[dict[str,Any]]):
    pass
