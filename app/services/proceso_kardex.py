from typing import Any
from sqlmodel import Session, col, select

from app.entities import KardexMovimientoBienConsumoEntity
from app.entities.KardexBienConsumoEntity import KardexBienConsumoEntity
from app.models.TipoEventosNats import EventoKardexBienConsumo


def procesar_movimientos_por_clave_evento(session: Session, evento: str, clave: str, almacen_uuid: str, bien_consumo_uuid: str, data: dict[str, Any]):
    match evento:
        
        case EventoKardexBienConsumo.CREAR_MOVIMIENTOS.value:
            movimientos: list[dict[str, Any]] = data.get("crear", []).get(clave, []).get("movimientos", [])
            kardex_id = _crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
            _crear_movimientos(session, kardex_id, movimientos )
            
        case EventoKardexBienConsumo.ACTUALIZAR_MOVIMIENTOS.value:
            movimientos_eliminar: list[dict[str, Any]] = data.get("eliminar", []).get(clave, []).get("movimientos", [])
            movimientos_crear: list[dict[str, Any]] = data.get("crear", []).get(clave, []).get("movimientos", [])
            kardex_id = _crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
            _actualizar_movimientos(session, kardex_id, movimientos_eliminar, movimientos_crear)
                
        case EventoKardexBienConsumo.ELIMINAR_MOVIMIENTOS.value:
            movimientos: list[dict[str, Any]] = data.get("eliminar", []).get(clave, []).get("movimientos", [])
            kardex_id = _crear_obtener_kardex(session, almacen_uuid, bien_consumo_uuid)
            _eliminar_movimientos(session, kardex_id, movimientos)
            
        case _:
            return None
        

def _crear_obtener_kardex(session: Session, almacen_uuid: str, bien_consumo_uuid: str) -> int:
    
    kardex = session.exec(
        select(KardexBienConsumoEntity).where(
            KardexBienConsumoEntity.almacen_uuid == almacen_uuid,
            KardexBienConsumoEntity.bien_consumo_uuid == bien_consumo_uuid
        )
    ).first()

    if kardex is None:
        data_id = session.exec(
            select(KardexBienConsumoEntity).order_by(col(KardexBienConsumoEntity.id).desc())
        ).first()
        
        id = 1 if data_id is None else data_id.id + 1
        
        session.add(KardexBienConsumoEntity(
            id=id,
            almacen_uuid=almacen_uuid,
            bien_consumo_uuid=bien_consumo_uuid
        ))
        
        return id
    
    return kardex.id
    

def get_movimiento_id(session: Session) -> int:
    data_id = session.exec(
        select(KardexMovimientoBienConsumoEntity).order_by(col(KardexMovimientoBienConsumoEntity.id).desc())
    ).first()
    
    return 1 if data_id is None else data_id.id + 1


def _crear_movimientos(session: Session, kardex_id: int, movimientos: list[dict[str,Any]]):
    session.add_all(
        KardexMovimientoBienConsumoEntity(
            id=get_movimiento_id(session),
            kardex_bien_consumo_id=kardex_id,
            movimiento_uuid=mov["movimientosUuid"],
            movimiento_ref_uuid=mov["movimientoRefUuid"],
            movimiento_tipo=mov["movimientoTipo"],
            fecha=mov["fecha"],
            documento_fuente_cod_serie=mov["documentoFuenteCodigoSerie"],
            documento_fuente_cod_numero=mov["documentoFuenteCodigoNumero"],
            concepto=mov["concepto"],
            entrada_cant=mov["entradaCantidad"],
            entrada_costo_uni=mov["entradaCostoUnitario"],
            entrada_costo_tot=mov["entradaCostoTotal"],
            salida_cant=mov["salidaCantidad"],
            salida_costo_uni=mov["salidaCostoUnitario"],
            salida_costo_tot=mov["salidaCostoTotal"],
        ) for mov in movimientos
    )
    pass

def _actualizar_movimientos(session: Session, kardex_id: int, movimientos_eliminar: list[dict[str,Any]], movimientos_crear: list[dict[str,Any]]):
    pass

def _eliminar_movimientos(session: Session, kardex_id: int, movimientos: list[dict[str,Any]]):
    pass


def procesar_movimientos(movimientos: list[dict[str,Any]]):
    # procesador_movimientos = ProcesadorMovimientos(df)
    pass