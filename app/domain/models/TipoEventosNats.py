from enum import Enum


class EventoKardexBienConsumo(Enum):
    CREAR_MOVIMIENTO = 'kardexBienConsumo.crearMovimiento'
    ACTUALIZAR_MOVIMIENTO = 'kardexBienConsumo.actualizarMovimiento'
    ELIMINAR_MOVIMIENTO = 'kardexBienConsumo.eliminarMovimiento'