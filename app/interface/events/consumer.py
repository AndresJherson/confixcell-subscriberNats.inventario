from typing import Any
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
import json
import asyncio

from app.domain.application.proceso_kardex import procesar_kardex_por_evento
from app.domain.dtos.WrapperKardexBienConsumoDTO import WrapperKardexBienConsumoDTO
from app.domain.models.TipoEventosNats import EventoKardexBienConsumo
from app.persistence.services.logger.logger import LOGGER
from config import get_env_NATS

async def wait_shutdown():

    _shutdown_event = asyncio.Event()

    def shutdown():
        print("Apagando...")
        _shutdown_event.set()
        
    try:
        await _shutdown_event.wait()
    except KeyboardInterrupt:
        shutdown()


async def iniciar_consumidor():
    nc = NATS()
    await nc.connect(get_env_NATS())

    def handler_kardex_bien_consumo(evento: str):
        async def handler(msg: Msg):
            try:
                payload: dict[str, Any] = json.loads(msg.data.decode())
                wrapperKardex = WrapperKardexBienConsumoDTO(**payload['data'])
                return await procesar_kardex_por_evento( evento, wrapperKardex)
            except Exception as e:
                LOGGER.error(f"Error en el handler de eventos 'handler_kardex_bien_consumo': {e}")
            
        return handler

    await nc.subscribe(EventoKardexBienConsumo.CREAR_MOVIMIENTO.value, cb=handler_kardex_bien_consumo(EventoKardexBienConsumo.CREAR_MOVIMIENTO.value))
    await nc.subscribe(EventoKardexBienConsumo.ELIMINAR_MOVIMIENTO.value, cb=handler_kardex_bien_consumo(EventoKardexBienConsumo.ELIMINAR_MOVIMIENTO.value))
    LOGGER.info("Escuchando eventos NATS...")
    
    await wait_shutdown()
    await nc.drain()
    LOGGER.info("Conexión NATS cerrada")