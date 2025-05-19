from typing import Any
from sqlmodel import Session
from app.models.TipoEventosNats import EventoKardexBienConsumo
from app.services.locks import intentar_bloquear_clave, liberar_clave
from services.persistencia_eventos import guardar_evento_kardex_pendiente
from app.database.database import engine_destino
                
async def procesar_evento(evento: str, data: dict[str, Any]):
    match evento:
        
        case EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value:
            record: dict[str, Any] = data["crear"]
            claves = list(record.keys())
            await _preprocesar_data(evento, claves, data)
            
        case EventoKardexBienConsumo.ACTUALIZAR_MOVIMIENTOS.value:
            record_eliminar: dict[str, Any] = data["eliminar"]
            record_crear: dict[str, Any] = data["crear"]
            claves_eliminar = list(record_eliminar.keys())
            claves_crear = list(record_crear.keys())
            claves = list(set(claves_eliminar + claves_crear))
            await _preprocesar_data(evento, claves, data)
            
        case EventoKardexBienConsumo.ELIMINAR_MOVIMIENTOS.value:
            record: dict[str, Any] = data["eliminar"]
            claves = list(record.keys())
            await _preprocesar_data(evento, claves, data)
            
        case _:
            return None
        

async def _preprocesar_data(evento: str, claves: list[str], data: dict[str, Any]):
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
                # función iniciar_procesamiento()
                # Lógica principal: actualizar kardex
                # 1. Obtener o crear kardex_bien_consumo
                # 2. Insertar detalles en orden
                # 3. Recalcular saldos con DataFrame si es necesario

                # Simulación de procesamiento
                print(f"Procesando evento para {clave}")

                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                # si es que hay eventos almacenados
                    # continuar el mismo proceso
                    # eliminar el evento almacenado
                # si no
                liberar_clave(session, clave)