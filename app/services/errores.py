import logging
from typing import cast
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ErrorKardexBienConsumoEntity
from app.services.persistencia import crear_obtener_kardex

async def registrar_error_kardex(
    session: AsyncSession,
    almacen_uuid: str,
    bien_consumo_uuid: str,
    mensaje: str
):
    try:
        kardex = await crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)

        error = ErrorKardexBienConsumoEntity(
            kardex_bien_consumo_id=cast(int, kardex.id),
            mensaje=mensaje,
        )
        session.add(error)
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Fallo al registrar el error en la tabla error_kardex_bien_consumo: {e}")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)