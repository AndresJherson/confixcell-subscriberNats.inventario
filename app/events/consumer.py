from typing import Any
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
from app.core.proceso_kardex import procesar_kardex_por_evento
from app.models import EventoKardexBienConsumo
from app.services.errores import logger
import json
import asyncio

from config import get_env_NATS

async def iniciar_consumidor():
    nc = NATS()
    await nc.connect(get_env_NATS())

    async def handler_kardex_bien_consumo(msg: Msg):
        try:
            data: dict[str, Any] = json.loads(msg.data.decode())
            return await procesar_kardex_por_evento( EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value, data)
        except Exception as e:
            logger.error(f"Error en el handler de eventos 'handler_kardex_bien_consumo': {e}")

    await nc.subscribe(EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value, cb=handler_kardex_bien_consumo)
    logger.info("Escuchando eventos NATS...")

    while True:
        await asyncio.sleep(1)
