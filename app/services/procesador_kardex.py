from typing import Any
from sqlmodel import Session
from app.entities.EventoPendienteKardexBienConsumoEntity import EventoPendienteKardexBienConsumoEntity
from app.models.TipoEventosNats import EventoKardexBienConsumo
from app.services.locks import intentar_bloquear_clave, liberar_clave
from app.services.proceso_kardex import procesar_movimientos_por_clave_evento
from services.persistencia_eventos import guardar_evento_kardex_pendiente, obtener_evento_kardex_pendiente
from app.database.database import engine_destino
                
async def procesar_kardex_por_evento(evento: str, data: dict[str, Any]) -> None:
    match evento:
        
        case EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value:
            record: dict[str, Any] = data["crear"]
            claves = list(record.keys())
            await _proceso_principal(evento, claves, data)
            
        case EventoKardexBienConsumo.ACTUALIZAR_MOVIMIENTOS.value:
            record_eliminar: dict[str, Any] = data["eliminar"]
            record_crear: dict[str, Any] = data["crear"]
            claves_eliminar = list(record_eliminar.keys())
            claves_crear = list(record_crear.keys())
            claves = list(set(claves_eliminar + claves_crear))
            await _proceso_principal(evento, claves, data)
            
        case EventoKardexBienConsumo.ELIMINAR_MOVIMIENTOS.value:
            record: dict[str, Any] = data["eliminar"]
            claves = list(record.keys())
            await _proceso_principal(evento, claves, data)
            
        case _:
            return None
        

async def _proceso_principal(evento: str, claves: list[str], data: dict[str, Any]):
    with Session(engine_destino) as session:
        for clave in claves:
            
            claves_split = clave.split("|")
            almacen_uuid = claves_split[0]
            bien_consumo_uuid = claves_split[1]
            
            resultado = await intentar_bloquear_clave(session, clave)
            if not resultado:
                await guardar_evento_kardex_pendiente(session, evento, almacen_uuid, bien_consumo_uuid, data)
                return

            try:
                print(f"Procesando evento para {clave}")
                evento_pendiente: EventoPendienteKardexBienConsumoEntity | None = None
                
                while True:
                    procesar_movimientos_por_clave_evento(session, evento, clave, almacen_uuid, bien_consumo_uuid, data)
                    
                    if evento_pendiente is not None:
                        session.delete(evento_pendiente)
                        
                    evento_pendiente = obtener_evento_kardex_pendiente(session, almacen_uuid, bien_consumo_uuid)
                    
                    if evento_pendiente is None:
                        break
                    
                    evento = evento_pendiente.evento
                    data = evento_pendiente.data
                                        
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                liberar_clave(session, clave)