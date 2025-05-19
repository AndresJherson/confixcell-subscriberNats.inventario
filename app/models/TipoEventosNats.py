from enum import Enum


class EventoKardexBienConsumo(Enum):
    CREAR_MOVIMIENTOS = 'bienConsumo.crearMovimientos'
    ACTUALIZAR_MOVIMIENTOS = 'bienConsumo.actualizarMovimientos'
    ELIMINAR_MOVIMIENTOS = 'bienConsumo.eliminarMovimientos'