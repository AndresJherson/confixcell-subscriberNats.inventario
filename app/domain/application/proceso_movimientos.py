from datetime import datetime, timezone
from typing import cast
from pandas import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.application.procesador_movimientos import ProcesadorMovimientos
from app.domain.dtos.KardexMovimientoBienConsumoDTO import KardexMovimientoBienConsumoDTO
from app.domain.dtos.WrapperKardexBienConsumoDTO import WrapperKardexBienConsumoDTO
from app.domain.models.TipoEventosNats import EventoKardexBienConsumo
from app.persistence.orms.KardexBienConsumoOrm import KardexBienConsumoOrm
from app.persistence.orms.KardexMovimientoBienConsumoOrm import KardexMovimientoBienConsumoOrm
from app.persistence.services.kardex_bien_consumo.kardex import KardexBienConsumoService
from app.persistence.services.kardex_bien_consumo.movimiento import KardexMovimientoBienConsumoService



async def procesar_movimientos_por_evento(session: AsyncSession, evento: str, clave: str, almacen_uuid: str, bien_consumo_uuid: str, wrapper: WrapperKardexBienConsumoDTO):
    match evento:
        
        case EventoKardexBienConsumo.CREAR_MOVIMIENTO.value:
            if wrapper.crear:
                movimientos: list[KardexMovimientoBienConsumoDTO] = wrapper.crear[clave].movimientos
                kardex = await KardexBienConsumoService.crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
                await _procesar_evento_crear(session, kardex, movimientos )
            
        case EventoKardexBienConsumo.ACTUALIZAR_MOVIMIENTO.value:
            if wrapper.crear and wrapper.eliminar:
                movimientos_crear: list[KardexMovimientoBienConsumoDTO] = wrapper.crear[clave].movimientos
                movimientos_eliminar: list[KardexMovimientoBienConsumoDTO] = wrapper.eliminar[clave].movimientos
                kardex = await KardexBienConsumoService.crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
                await _procesar_evento_actualizar(session, kardex, movimientos_eliminar, movimientos_crear)
                
        case EventoKardexBienConsumo.ELIMINAR_MOVIMIENTO.value:
            if wrapper.eliminar:
                movimientos: list[KardexMovimientoBienConsumoDTO] = wrapper.eliminar[clave].movimientos
                kardex = await KardexBienConsumoService.crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
                await _procesar_evento_eliminar(session, kardex, movimientos)
            
        case _:
            return None
    

async def _procesar_evento_crear(session: AsyncSession, kardex: KardexBienConsumoOrm, movimientos: list[KardexMovimientoBienConsumoDTO]):
    fecha_minima = await KardexMovimientoBienConsumoService.crear_movimientos(session, cast(int,kardex.id), movimientos)
    if fecha_minima:
        await _procesar_movimientos(session, kardex, fecha_minima)


async def _procesar_evento_actualizar(session: AsyncSession, kardex: KardexBienConsumoOrm, movimientos_eliminar: list[KardexMovimientoBienConsumoDTO], movimientos_crear: list[KardexMovimientoBienConsumoDTO]):
    fecha_1 = await KardexMovimientoBienConsumoService.eliminar_movimientos_by_movimiento_uuid(session, movimientos_eliminar)
    fecha_2 = await KardexMovimientoBienConsumoService.crear_movimientos(session, cast(int,kardex.id), movimientos_crear)
    fecha_minima = None
    
    if fecha_1 is None and fecha_2 is None:
        return
    elif fecha_1 is None and fecha_2 is not None:
        fecha_minima = fecha_2
    elif fecha_1 is not None and fecha_2 is None:
        fecha_minima = fecha_1
    elif fecha_1 is not None and fecha_2 is not None:
        fecha_minima = min([fecha_1, fecha_2])
        
    if fecha_minima:
        await _procesar_movimientos(session, kardex, fecha_minima)


async def _procesar_evento_eliminar(session: AsyncSession, kardex: KardexBienConsumoOrm, movimientos: list[KardexMovimientoBienConsumoDTO]):
    fecha_minima = await KardexMovimientoBienConsumoService.eliminar_movimientos_by_movimiento_uuid(session, movimientos)
    if fecha_minima:
        await _procesar_movimientos(session, kardex, fecha_minima)


async def _procesar_movimientos(session: AsyncSession, kardex: KardexBienConsumoOrm, fecha: datetime):
    anterior_ultimo_movimiento = await KardexMovimientoBienConsumoService.obtener_movimiento_anterior_fecha(session, cast(int,kardex.id), fecha)
    ultimo_movimiento = anterior_ultimo_movimiento if anterior_ultimo_movimiento is not None else KardexMovimientoBienConsumoOrm(
        uuid='',
        kardex_bien_consumo_id=0,
        movimiento_uuid='',
        movimiento_tipo='',
        fecha=datetime.now(),
        documento_fuente_cod_serie='',
        documento_fuente_cod_numero=0
    )
    
    offset = 0
    limit = 100
    procesador = ProcesadorMovimientos(DataFrame(), ultimo_movimiento)
    
    while True:

        data = await KardexMovimientoBienConsumoService.obtener_lote_movimientos_desde_fecha(session, cast(int,kardex.id), fecha, offset, limit)
        if len(data) == 0:
            break
        
        df = DataFrame([x.model_dump() for x in data])
        procesador.set_df(df)
        procesador.procesar()
        
        await KardexMovimientoBienConsumoService.actualizar_movimientos_desde_dataframe(session, df)
        
        offset += limit
        
    kardex.entrada_cant_acumulado = procesador.entrada_cant_acumulado
    kardex.entrada_costo_acumulado = procesador.entrada_costo_acumulado
    
    kardex.salida_cant_acumulado = procesador.salida_cant_acumulado
    kardex.salida_costo_acumulado = procesador.salida_costo_acumulado
    
    kardex.saldo_cant = procesador.saldo_cant
    kardex.saldo_valor_uni = procesador.saldo_valor_uni
    kardex.saldo_valor_tot = procesador.saldo_valor_tot
    kardex.f_actualizacion = datetime.now(timezone.utc)