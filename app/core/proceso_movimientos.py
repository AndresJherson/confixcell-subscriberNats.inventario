from typing import Any, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import EventoKardexBienConsumo
from app.services.persistencia import crear_movimientos, crear_obtener_kardex, eliminar_movimientos_by_uuids


async def procesar_movimientos_por_evento(session: AsyncSession, evento: str, clave: str, almacen_uuid: str, bien_consumo_uuid: str, data: dict[str, Any]):
    match evento:
        
        case EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value:
            movimientos: list[dict[str, Any]] = data.get("crear", []).get(clave, []).get("movimientos", [])
            kardex = await crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
            await _procesar_evento_crear(session, cast(int, kardex.id), movimientos )
            
        case EventoKardexBienConsumo.ACTUALIZAR_MOVIMIENTOS.value:
            movimientos_eliminar: list[dict[str, Any]] = data.get("eliminar", []).get(clave, []).get("movimientos", [])
            movimientos_crear: list[dict[str, Any]] = data.get("crear", []).get(clave, []).get("movimientos", [])
            kardex = await crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
            await _procesar_evento_actualizar(session, cast(int, kardex.id), movimientos_eliminar, movimientos_crear)
                
        case EventoKardexBienConsumo.ELIMINAR_MOVIMIENTOS.value:
            movimientos: list[dict[str, Any]] = data.get("eliminar", []).get(clave, []).get("movimientos", [])
            kardex = await crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
            await _procesar_evento_eliminar(session, cast(int, kardex.id), movimientos)
            
        case _:
            return None
    

async def _procesar_evento_crear(session: AsyncSession, kardex_id: int, movimientos: list[dict[str,Any]]):
    await crear_movimientos(session, kardex_id, movimientos)
    pass

async def _procesar_evento_actualizar(session: AsyncSession, kardex_id: int, movimientos_eliminar: list[dict[str,Any]], movimientos_crear: list[dict[str,Any]]):
    pass

async def _procesar_evento_eliminar(session: AsyncSession, kardex_id: int, movimientos: list[dict[str,Any]]):
    await eliminar_movimientos_by_uuids(session, movimientos)
    pass
