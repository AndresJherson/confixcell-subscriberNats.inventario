from typing import Any
from pandas import DataFrame, Series
from sqlmodel import Session

from app.models.MovimientoTipoBienConsumo import MovimientoTipoBienConsumo

class ProcesadorMovimientos:
    
    def __init__(self, df: DataFrame, session: Session):
        self.df = df
        self.session = session
        
    def set_df(self, df: DataFrame):
        self.df = df
        
    def procesar(self):
        for index, row in self.df.iterrows():
            match row["movimiento_tipo"]:
        
                case MovimientoTipoBienConsumo.ENTRADA_VALOR_NUEVO.value:
                    self.procesar_entrada_bien_consumo_valor_nuevo(row)
                    
                case MovimientoTipoBienConsumo.ENTRADA_VALOR_SALIDA.value:
                    self.procesar_entrada_bien_consumo_valor_nuevo(row)
                        
                case MovimientoTipoBienConsumo.SALIDA_VALOR_NUEVO.value:
                    self.procesar_entrada_bien_consumo_valor_nuevo(row)
                    
                case MovimientoTipoBienConsumo.SALIDA_VALOR_ENTRADA.value:
                    self.procesar_entrada_bien_consumo_valor_nuevo(row)
                    
                case MovimientoTipoBienConsumo.SALIDA_NOTA_VENTA.value:
                    self.procesar_entrada_bien_consumo_valor_nuevo(row)
                    
                case MovimientoTipoBienConsumo.SALIDA_NOTA_VENTA_SERVICIO_REPARACION_RECURSO.value:
                    self.procesar_entrada_bien_consumo_valor_nuevo(row)
                    
                case '':
                    continue

    def procesar_entrada_bien_consumo_valor_nuevo(self, row: Series[Any]):
        pass

    def procesar_entrada_bien_consumo_valor_salida(self, row: Series[Any]):
        pass

    def procesar_salida_bien_consumo_valor_nuevo(self, row: Series[Any]):
        pass

    def procesar_salida_bien_consumo_valor_entrada(self, row: Series[Any]):
        pass

    def procesar_nv_salida_bien_consumo(self, row: Series[Any]):
        pass

    def procesar_nv_servicio_reparacion_recurso_bien_consumo(self, movimiento: dict[str,Any]):
        pass
    
    
    def actualizar(self):
        # reemplazar los movimientos actualizados a la db
        pass