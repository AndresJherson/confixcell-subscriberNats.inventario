from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4
from pandas import DataFrame
from sqlalchemy import delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from app.domain.dtos.KardexMovimientoBienConsumoDTO import KardexMovimientoBienConsumoDTO
from app.persistence.orms.KardexMovimientoBienConsumoOrm import KardexMovimientoBienConsumoOrm

class KardexMovimientoBienConsumoService:
    
    @staticmethod
    async def crear_movimientos(session: AsyncSession, kardex_id: int, movimientos: list[KardexMovimientoBienConsumoDTO]):

        if len(movimientos) == 0:
            return None
        
        movimientos_ordenados = sorted(movimientos, key=lambda x: x.fecha.astimezone(timezone.utc))
        session.add_all(KardexMovimientoBienConsumoOrm(
            uuid=str(uuid4()),
            kardex_bien_consumo_id=kardex_id,
            movimiento_uuid=mov.movimientoUuid,
            movimiento_ref_uuid=mov.movimientoRefUuid,
            movimiento_tipo=mov.movimientoTipo,
            fecha=mov.fecha.astimezone(timezone.utc),
            documento_fuente_cod_serie=mov.documentoFuenteCodigoSerie,
            documento_fuente_cod_numero=mov.documentoFuenteCodigoNumero,
            concepto=mov.concepto,
            entrada_cant=mov.entradaCantidad,
            entrada_costo_uni=mov.entradaCostoUnitario,
            entrada_costo_tot=mov.entradaCostoTotal,
            salida_cant=mov.salidaCantidad,
            salida_costo_uni=mov.salidaCostoUnitario,
            salida_costo_tot=mov.salidaCostoTotal
        ) for mov in movimientos_ordenados)
        
        return movimientos_ordenados[0].fecha
    
    
    @staticmethod
    async def eliminar_movimientos_by_movimiento_uuid(session: AsyncSession, movimientos: list[KardexMovimientoBienConsumoDTO]):
        uuids = list(map(lambda x: x.movimientoUuid, movimientos))
        
        result = await session.execute(
            select(func.min(KardexMovimientoBienConsumoOrm.fecha))
            .where(col(KardexMovimientoBienConsumoOrm.movimiento_uuid).in_(uuids))
        )
        fecha = result.scalars().first()
        
        await session.execute(
            delete(KardexMovimientoBienConsumoOrm)
            .where(col(KardexMovimientoBienConsumoOrm.movimiento_uuid).in_(uuids))
        )
        
        return fecha


    @staticmethod
    async def obtener_movimiento_anterior_fecha(session: AsyncSession, kardex_id: int, fecha: datetime):
        result = await session.execute(
            select(KardexMovimientoBienConsumoOrm)
            .where(KardexMovimientoBienConsumoOrm.kardex_bien_consumo_id == kardex_id)
            .where(KardexMovimientoBienConsumoOrm.fecha < fecha)
            .order_by(col(KardexMovimientoBienConsumoOrm.fecha).desc(), col(KardexMovimientoBienConsumoOrm.id).desc())
            .limit(1)
        )
        return result.scalar_one_or_none()    


    @staticmethod
    async def obtener_lote_movimientos_desde_fecha(session: AsyncSession, kardex_id: int, fecha: datetime, offset: int, limit: int):
        result = await session.execute(
            select(KardexMovimientoBienConsumoOrm)
            .where(KardexMovimientoBienConsumoOrm.kardex_bien_consumo_id == kardex_id)
            .where(KardexMovimientoBienConsumoOrm.fecha >= fecha)
            .order_by(col(KardexMovimientoBienConsumoOrm.fecha).asc(), col(KardexMovimientoBienConsumoOrm.id).asc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()


    @staticmethod
    async def actualizar_movimientos_desde_dataframe(session: AsyncSession, df: DataFrame) -> Optional[datetime]:
        if df.empty:
            return None
        
        for _, row in df.iterrows():
            await session.execute(
                update(KardexMovimientoBienConsumoOrm)
                .where(KardexMovimientoBienConsumoOrm.id == int(row['id'])) # type: ignore
                .values(                
                    entrada_cant = row['entrada_cant'], # type: ignore
                    entrada_costo_uni = row['entrada_costo_uni'], # type: ignore
                    entrada_costo_tot = row['entrada_costo_tot'], # type: ignore
                    entrada_cant_acumulado = row['entrada_cant_acumulado'], # type: ignore
                    entrada_costo_acumulado = row['entrada_costo_acumulado'], # type: ignore
                    salida_cant = row['salida_cant'], # type: ignore
                    salida_costo_uni = row['salida_costo_uni'], # type: ignore
                    salida_costo_tot = row['salida_costo_tot'], # type: ignore
                    salida_cant_acumulado = row['salida_cant_acumulado'], # type: ignore
                    salida_costo_acumulado = row['salida_costo_acumulado'], # type: ignore
                    saldo_cant = row['saldo_cant'], # type: ignore
                    saldo_valor_uni = row['saldo_valor_uni'], # type: ignore
                    saldo_valor_tot = row['saldo_valor_tot'] # type: ignore
                )
            )