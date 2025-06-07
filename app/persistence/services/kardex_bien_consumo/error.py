from typing import cast
from uuid import uuid4

from app.persistence.database.database import get_session_destino
from app.persistence.orms.ErrorKardexBienConsumoOrm import ErrorKardexBienConsumoOrm
from app.persistence.services.kardex_bien_consumo.kardex import KardexBienConsumoService
from app.persistence.services.logger.logger import LOGGER

class ErrorKardexBienConsumoService:

    @staticmethod
    async def registrar_error(
        almacen_uuid: str,
        bien_consumo_uuid: str,
        mensaje: str
    ):
        async with get_session_destino() as session:
            try:
                kardex = await KardexBienConsumoService.crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)

                error = ErrorKardexBienConsumoOrm(
                    uuid=str(uuid4()),
                    kardex_bien_consumo_id=cast(int, kardex.id),
                    mensaje=mensaje,
                )
                session.add(error)
                await session.commit()
            except Exception as e:
                await session.rollback()
                LOGGER.error(f"Fallo al registrar el error en la tabla error_kardex_bien_consumo: {e}")