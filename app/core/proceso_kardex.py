from app.core.proceso_movimientos import procesar_movimientos_por_evento
from app.entities import EventoPendienteKardexBienConsumoEntity
from app.services.errores import logger
from typing import Any
from app.models.TipoEventosNats import EventoKardexBienConsumo
from app.services.errores import registrar_error_kardex
from app.services.locks import intentar_bloquear_clave, liberar_clave
from app.database.database import get_session_destino
from app.services.persistencia import guardar_evento_kardex_pendiente, obtener_evento_kardex_pendiente

async def procesar_kardex_por_evento(evento: str, data: dict[str, Any]) -> None:
    match evento:
        
        case EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value:
            record: dict[str, Any] = data.get("crear", {})
            claves = list(record.keys())
            await _proceso_principal(evento, claves, data)
            
        case EventoKardexBienConsumo.ACTUALIZAR_MOVIMIENTOS.value:
            record_eliminar: dict[str, Any] = data.get("eliminar", {})
            record_crear: dict[str, Any] = data.get("crear", {})
            claves_eliminar = list(record_eliminar.keys())
            claves_crear = list(record_crear.keys())
            claves = list(set(claves_eliminar + claves_crear))
            await _proceso_principal(evento, claves, data)
            
        case EventoKardexBienConsumo.ELIMINAR_MOVIMIENTOS.value:
            record: dict[str, Any] = data.get("eliminar", {})
            claves = list(record.keys())
            await _proceso_principal(evento, claves, data)
            
        case _:
            return None
        

async def _proceso_principal(evento: str, claves: list[str], data: dict[str, Any]):
    for clave in claves:
        
        almacen_uuid, bien_consumo_uuid = clave.split("|")
        if len(almacen_uuid) == 0 and len(bien_consumo_uuid) == 0:
            logger.error("Clave inválido")
            continue

        async with get_session_destino() as session:
            resultado = await intentar_bloquear_clave(session, clave)
            if not resultado:
                await guardar_evento_kardex_pendiente(session, evento, almacen_uuid, bien_consumo_uuid, data)
                continue

        logger.info(f"Procesando evento para {clave}")
        evento_pendiente: EventoPendienteKardexBienConsumoEntity | None = None
        
        while True:
            async with get_session_destino() as session:
                try:
                    
                    await procesar_movimientos_por_evento(session, evento, clave, almacen_uuid, bien_consumo_uuid, data)
                    if evento_pendiente is not None:
                        await session.delete(evento_pendiente)
                    await session.commit()
                    
                    evento_pendiente = await obtener_evento_kardex_pendiente(session, almacen_uuid, bien_consumo_uuid)
                    if evento_pendiente is None:
                        await liberar_clave(session, clave)
                        break
                    
                    evento = evento_pendiente.evento
                    data = evento_pendiente.data

                except Exception as e:
                    await session.rollback()
                    await registrar_error_kardex(session, almacen_uuid, bien_consumo_uuid, str(e))
