from enum import Enum


class MovimientoTipoBienConsumo(Enum):
    ENTRADA_VALOR_NUEVO = 'EntradaBienConsumoValorNuevo'
    ENTRADA_VALOR_SALIDA = 'EntradaBienConsumoValorSalida'
    SALIDA_VALOR_NUEVO = 'SalidaBienConsumoValorNuevo'
    SALIDA_VALOR_ENTRADA = 'SalidaBienConsumoValorEntrada'
    SALIDA_NOTA_VENTA = 'NotaVentaSalidaBienConsumo'
    SALIDA_NOTA_VENTA_SERVICIO_REPARACION_RECURSO = 'NotaVentaSalidaProduccionServicioReparacionRecursoBienConsumo'