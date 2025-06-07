from app.domain.application.proceso_movimientos import procesar_movimientos_por_evento
from app.domain.dtos.WrapperKardexBienConsumoDTO import WrapperKardexBienConsumoDTO
from app.domain.models.TipoEventosNats import EventoKardexBienConsumo
from app.persistence.database.database import get_session_destino
from app.persistence.orms.EventoPendienteKardexBienConsumoOrm import EventoPendienteKardexBienConsumoOrm
from app.persistence.services.kardex_bien_consumo.error import ErrorKardexBienConsumoService
from app.persistence.services.kardex_bien_consumo.evento_pendiente import EventoPendienteKardexBienConsumoService
from app.persistence.services.kardex_bien_consumo.kardex_lock import KardexLockService
from app.persistence.services.logger.logger import LOGGER


async def procesar_kardex_por_evento(evento: str, wrapper: WrapperKardexBienConsumoDTO) -> None:
    match evento:
        
        case EventoKardexBienConsumo.CREAR_MOVIMIENTO.value:
            if wrapper.crear:
                claves = list(wrapper.crear.keys())
                await _proceso_principal(evento, claves, wrapper)
            
        case EventoKardexBienConsumo.ACTUALIZAR_MOVIMIENTO.value:
            if wrapper.crear and wrapper.eliminar:
                claves_eliminar = list(wrapper.eliminar.keys())
                claves_crear = list(wrapper.crear.keys())
                claves = list(set(claves_eliminar + claves_crear))
                await _proceso_principal(evento, claves, wrapper)
            
        case EventoKardexBienConsumo.ELIMINAR_MOVIMIENTO.value:
            if wrapper.eliminar:
                claves = list(wrapper.eliminar.keys())
                await _proceso_principal(evento, claves, wrapper)
            
        case _:
            return None
        

async def _proceso_principal(evento: str, claves: list[str], wrapper: WrapperKardexBienConsumoDTO):
    for clave in claves:
        
        almacen_uuid, bien_consumo_uuid = clave.split("|")
        if len(almacen_uuid) == 0 and len(bien_consumo_uuid) == 0:
            LOGGER.error("Clave inválido")
            continue

        resultado = await KardexLockService.intentar_bloquear_clave(clave)
        if not resultado:
            await EventoPendienteKardexBienConsumoService.guardar_evento_pendiente(evento, almacen_uuid, bien_consumo_uuid, wrapper)
            continue

        LOGGER.info(f"Procesando evento para {clave}")
        evento_pendiente: EventoPendienteKardexBienConsumoOrm | None = None
        
        while True:
            async with get_session_destino() as session:
                try:
                    await procesar_movimientos_por_evento(session, evento, clave, almacen_uuid, bien_consumo_uuid, wrapper)
                    if evento_pendiente is not None:
                        await session.delete(evento_pendiente)
                    await session.commit()
                    
                    evento_pendiente = await EventoPendienteKardexBienConsumoService.obtener_evento_pendiente(session, almacen_uuid, bien_consumo_uuid)
                    if evento_pendiente is None:
                        await KardexLockService.liberar_clave(clave)
                        break
                    
                    evento = evento_pendiente.evento
                    wrapper = WrapperKardexBienConsumoDTO(**evento_pendiente.data)

                except Exception as e:
                    await session.rollback()
                    await ErrorKardexBienConsumoService.registrar_error(almacen_uuid, bien_consumo_uuid, str(e))
                    LOGGER.error(f"Error en el evento de {clave} \n{str(e)}")
                    
        LOGGER.info(f"Proceso exitoso para {clave}")