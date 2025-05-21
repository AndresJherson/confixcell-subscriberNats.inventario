from typing import Any
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
from app.models.TipoEventosNats import EventoKardexBienConsumo
from app.services.proceso_kardex import procesar_kardex_por_evento
import json
import asyncio

async def iniciar_consumidor():
    nc = NATS()
    await nc.connect("nats://localhost:4222")

    async def mensaje_handler(msg: Msg):
        data: dict[str, Any] = json.loads(msg.data.decode())
        return await procesar_kardex_por_evento( EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value, data)

    await nc.subscribe(EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value, cb=mensaje_handler)
    print("Escuchando eventos NATS...")

    while True:
        await asyncio.sleep(1)
